from functools import lru_cache

import json


@lru_cache
def get_queries_file(file_path):
    with open(file_path, "r") as fobj:
        return json.load(fobj)
