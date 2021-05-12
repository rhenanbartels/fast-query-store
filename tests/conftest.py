import logging
import os
from contextlib import suppress
from tempfile import NamedTemporaryFile

import pytest
import sqlalchemy
from sqlalchemy import create_engine
from starlette.testclient import TestClient

from app.main import app
from tests import test_settings


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def queries_json_file():
    queries_file = NamedTemporaryFile(suffix=".json", delete=False)
    yield queries_file


@pytest.fixture(scope="module")
def db_url():
    yield os.path.join(
            test_settings.TEST_POSTGRES_SERVICE_URL,
            test_settings.TEST_POSTGRES_DB_NAME,
    )


@pytest.fixture(scope="module")
def database_engine(db_url):
    logger.info("creating test database...")
    engine = create_engine(
            test_settings.TEST_POSTGRES_SERVICE_URL,
            isolation_level="AUTOCOMMIT"
    )
    with engine.connect() as conn, suppress(sqlalchemy.exc.ProgrammingError):
        conn.execute(f"CREATE DATABASE {test_settings.TEST_POSTGRES_DB_NAME}")

    db_engine = create_engine(db_url)
    yield db_engine

    logger.info("destroying test database...")
    db_engine.dispose()
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {test_settings.TEST_POSTGRES_DB_NAME}")
