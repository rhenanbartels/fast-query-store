import json
from functools import lru_cache
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy import create_engine

from app import backends
from app.config import Settings
from app.exceptions import QueryNotFoundError

app = FastAPI()


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

    db_engine = create_engine(query["db_url"])
    with db_engine.connect() as conn:
        result_set = jsonable_encoder(conn.execute(query["query"]).fetchall())

    db_engine.dispose()

    return {"result_set": result_set}
