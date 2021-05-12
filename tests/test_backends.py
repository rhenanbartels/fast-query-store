import json
import os
from tempfile import NamedTemporaryFile
from unittest import mock

import pytest

from app.backends import JsonBackend
from app.exceptions import QueryNotFoundError


class TestJsonBackend:
    @pytest.fixture(scope="class")
    def setup(self):
        queries_file = NamedTemporaryFile(suffix=".json", delete=False)

        query_slug = "query-slug-1"
        query_cmd = "SELECT * FROM products"
        db_url = "db_url"
        json_content = {
            query_slug: {
                "query": query_cmd,
                "db_url": db_url,
            },
        }
        file_path = queries_file.name
        with open(file_path, "w") as fobj:
            json.dump(json_content, fobj)

        fixtures = {
            "file_path": file_path,
            "json_content": json_content,
            "query_slug": query_slug,
            "query_cmd": query_cmd,
        }
        yield fixtures

    @pytest.mark.asyncio
    async def test_open_queries_file(self, setup):
        backend = JsonBackend(file_path=setup["file_path"])
        queries = await backend.queries

        assert queries == setup["json_content"]

    @pytest.mark.asyncio
    async def test_get_query_by_slug(self, setup):
        backend = JsonBackend(file_path=setup["file_path"])
        query = await backend.get_query(setup["query_slug"])

        assert query == setup["json_content"][setup["query_slug"]]

    @pytest.mark.asyncio
    async def test_raise_exception_if_query_doesn_exist(self, setup):
        backend = JsonBackend(file_path=setup["file_path"])

        with pytest.raises(QueryNotFoundError):
            await backend.get_query("missing-query")

    @pytest.mark.asyncio
    async def test_read_db_url_from_env_var(self, setup):
        env_var = "${DB_URL}"
        db_url = "postgresql://user:pwd@localhost:5432/db"
        setup["json_content"][setup["query_slug"]]["db_url"] = env_var
        with open(setup["file_path"], "w") as fobj:
            json.dump(setup["json_content"], fobj)

        backend = JsonBackend(file_path=setup["file_path"])
        with mock.patch.dict(os.environ, {"DB_URL": db_url}):
            query = await backend.get_query(setup["query_slug"])

        assert query["db_url"] == db_url
