import json

from app import config, main


def test_root_route(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "hello world"


def test_execute_query_from_query_slug_request(test_client, queries_json_file):
    query_slug = "query-slug-1"
    query_cmd = "SELECT * FROM dual"
    json_content = {
        query_slug: {
            "query": query_cmd,
        },
    }
    with open(queries_json_file.name, "w") as fobj:
        json.dump(json_content, fobj)

    def get_settings_override():
        return config.Settings(queries_file_path=queries_json_file.name)

    main.app.dependency_overrides[main.get_settings] = get_settings_override

    query_slug = "query-slug-1"
    response = test_client.get(f"/{query_slug}")

    assert response.status_code == 200
    assert response.json()["query_cmd"] == query_cmd
