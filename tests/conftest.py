from tempfile import NamedTemporaryFile

import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def queries_json_file():
    queries_file = NamedTemporaryFile(suffix=".json", delete=False)
    yield queries_file
