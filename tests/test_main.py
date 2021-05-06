def test_root_route(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "hello world"


def test_execute_query_from_query_slug_request(test_client):
    query_slug = "query-slug-1"
    response = test_client.get(f"/{query_slug}")

    assert response.status_code == 200
    assert response.json()["slug"] == query_slug
