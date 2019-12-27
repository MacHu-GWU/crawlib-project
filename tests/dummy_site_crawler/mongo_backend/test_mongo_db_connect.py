# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site_crawler.mongo_backend.db import db


def test():
    col = db["test"]
    col.update_one({"_id": 1}, {"$set": {"value": "Hello World!"}}, upsert=True)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
