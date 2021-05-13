import json
import os
import pathlib
import re
from functools import cached_property
from typing import Dict, Union

import aiofiles

from app.exceptions import QueryNotFoundError


class JsonBackend:
    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        self.file_path = file_path

    @cached_property
    async def queries(self) -> None:
        async with aiofiles.open(self.file_path, "r") as fobj:
            content = json.loads(await fobj.read())

        return content

    async def get_db_url(self, url):
        _url = url
        match = re.search(r"\${(.*?)}", url)
        if match:
            env_var_name = match.group(1)
            _url = os.environ[env_var_name]

        return _url

    async def get_query(self, slug: str) -> Dict:
        queries = await self.queries
        if slug not in queries:
            raise QueryNotFoundError

        query = queries[slug]
        query["db_url"] = await self.get_db_url(query["db_url"])
        return query
