import json
from functools import lru_cache
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine

from app import backends
from app.config import Settings
from app.exceptions import QueryNotFoundError

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "hello world"}


# TODO: create db connections pool. (Maybe use a dict)
@app.get("/query/{slug}")
async def execute(slug: str, settings: Settings = Depends(get_settings)):
    backend = backends.JsonBackend(file_path=settings.queries_file_path)
    try:
        query = await backend.get_query(slug)
    except QueryNotFoundError:
        raise HTTPException(status_code=404, detail=f"Query '{slug}' not found")

    db_engine = create_engine(query["db_url"])
    with db_engine.connect() as conn:
        result_set = conn.execute(query["query"]).fetchall()

    db_engine.dispose()

    return {"result_set": result_set}
