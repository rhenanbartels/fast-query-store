import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    queries_file_path: str = os.getenv("queries_file_path", "")
