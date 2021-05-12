import pathlib
import os
import re
from functools import cached_property, lru_cache
from typing import Dict, Union

import json

from app.exceptions import QueryNotFoundError


class JsonBackend:
    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        self.file_path = file_path

    @cached_property
    def queries(self) -> None:
        with open(self.file_path, "r") as fobj:
            content = json.load(fobj)

        return content

    def get_db_url(self, url):
        _url = url
        match = re.search(r"\${(.*?)}", url)
        if match:
            env_var_name = match.group(1)
            _url = os.environ[env_var_name]

        return _url

    def get_query(self, slug: str) -> Dict:
        if slug not in self.queries:
            raise QueryNotFoundError

        query = self.queries[slug]
        query["db_url"] = self.get_db_url(query["db_url"])
        return query
