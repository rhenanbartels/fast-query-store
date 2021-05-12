import json
import os
from unittest import mock

import pytest

from app import config, main
from tests import test_settings


class TestMain:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, database_engine):
        drop_tb = """
            DROP TABLE IF EXISTS products;
        """
        create_tb = """
            CREATE TABLE IF NOT EXISTS products (
                product_no integer,
                name text,
                price numeric
            );
        """
        insert_data = """
            INSERT INTO products (product_no, name, price) VALUES
            (1, 'Cheese', 9.99),
            (2, 'Bread', 1.99),
            (3, 'Milk', 2.99);
        """
        database_engine.execute(drop_tb)
        database_engine.execute(create_tb)
        database_engine.execute(insert_data)

    def test_root_route(self, test_client):
        response = test_client.get("/")

        assert response.status_code == 200
        assert response.json()["message"] == "hello world"

    def test_execute_query_from_query_slug_request(
        self,
        test_client,
        queries_json_file,
        database_engine,
        db_url,
    ):
        query_slug = "query-slug-1"
        query_cmd = "SELECT * FROM products"
        json_content = {
            query_slug: {
                "query": query_cmd,
                "db_url": db_url,
            },
        }
        with open(queries_json_file.name, "w") as fobj:
            json.dump(json_content, fobj)

        def get_settings_override():
            return config.Settings(queries_file_path=queries_json_file.name)

        main.app.dependency_overrides[main.get_settings] = get_settings_override

        query_slug = "query-slug-1"
        response = test_client.get(f"/query/{query_slug}")
        expected_rs = [
            {"product_no": 1, "name": "Cheese", "price": 9.99},
            {"product_no": 2, "name": "Bread", "price": 1.99},
            {"product_no": 3, "name": "Milk", "price": 2.99},
        ]

        assert response.status_code == 200
        assert response.json()["result_set"] == expected_rs

    def test_fill_db_url_in_json_with_env_var(
        self,
        test_client,
        queries_json_file,
        database_engine,
        db_url,
    ):
        query_slug = "query-slug-1"
        query_cmd = "SELECT * FROM products"
        json_content = {
            query_slug: {
                "query": query_cmd,
                "db_url": "${DATABASE_ENV_VARIABLE}",
            },
        }
        with open(queries_json_file.name, "w") as fobj:
            json.dump(json_content, fobj)

        def get_settings_override():
            return config.Settings(queries_file_path=queries_json_file.name)

        main.app.dependency_overrides[main.get_settings] = get_settings_override

        query_slug = "query-slug-1"
        with mock.patch.dict(os.environ, {"DATABASE_ENV_VARIABLE": db_url}):
            response = test_client.get(f"/query/{query_slug}")

        expected_rs = [
            {"product_no": 1, "name": "Cheese", "price": 9.99},
            {"product_no": 2, "name": "Bread", "price": 1.99},
            {"product_no": 3, "name": "Milk", "price": 2.99},
        ]

        assert response.status_code == 200
        assert response.json()["result_set"] == expected_rs

    def test_return_404_when_slug_doesnt_exist(self, test_client):
        query_slug = "missing-slug"
        response = test_client.get(f"/query/{query_slug}")

        assert response.status_code == 404
