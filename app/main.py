import logging
from functools import lru_cache

import sqlalchemy
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from sqlalchemy.exc import OperationalError, ProgrammingError

from app import backends
from app.config import Settings
from app.exceptions import QueryNotFoundError

app = FastAPI()
logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return Settings()


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    backend = backends.JsonBackend(file_path=settings.queries_file_path)
    queries = await backend.queries
    slugs = sorted(queries.keys())
    return {"slugs": slugs}


@app.get("/query/{slug}")
@cache(expire=get_settings().cache_ttl)
async def execute(slug: str, settings: Settings = Depends(get_settings)):
    backend = backends.JsonBackend(file_path=settings.queries_file_path)
    try:
        query = await backend.get_query(slug)
    except QueryNotFoundError:
        raise HTTPException(status_code=404, detail=f"Query '{slug}' not found")

    db_engine = sqlalchemy.create_engine(query["db_url"])
    with db_engine.connect() as conn:
        try:
            result_set = jsonable_encoder(conn.execute(query["query"]).fetchall())
        except (ProgrammingError, OperationalError) as e:
            logger.error(f"{e!r}")
            raise HTTPException(status_code=500, detail="Server side error")
        finally:
            conn.close()
            db_engine.dispose()

    return {"result_set": result_set}
