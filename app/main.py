import json
from functools import lru_cache
from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

from app import backends
from app.config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "hello world"}


# TODO: create db connections pool. (Maybe use a dict)
# TODO: create result set serializer
@app.get("/{slug}")
async def execute(slug: str, settings: Settings = Depends(get_settings)):
    queries_file = backends.get_queries_file(settings.queries_file_path)
    db_engine = create_engine(queries_file[slug]["db_url"])
    with db_engine.connect() as conn:
        result_set = conn.execute(queries_file[slug]["query"]).fetchall()

    return {"result_set": result_set}
