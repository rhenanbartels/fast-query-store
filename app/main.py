import json
from functools import lru_cache

from fastapi import Depends, FastAPI

from app import backends
from app.config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/{slug}")
async def execute(slug: str, settings: Settings = Depends(get_settings)):
    queries_file = backends.get_queries_file(settings.queries_file_path)
    return {"query_cmd": queries_file[slug]["query"]}
