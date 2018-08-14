#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
import shutil
from crawlib.cache import create_cache, CacheBackedSpider

cache_dir = os.path.join(os.path.dirname(__file__), ".cache")


def setup_module():
    try:
        shutil.rmtree(cache_dir)
    except:
        pass


def test_create_cache():
    key = "https://www.python.org"
    value = '<div class="header">Python is awesome!</div>'

    # value is unicode
    cache = create_cache(cache_dir, value_type_is_binary=False)
    cache.set(key, value)
    assert cache[key] == value
    cache.close()

    # value is bytes
    cache = create_cache(cache_dir, value_type_is_binary=True)
    cache.set(key, value.encode("utf-8"))
    assert cache[key] == value.encode("utf-8")
    cache.close()


def test_CacheBackedSpider():
    with CacheBackedSpider(cache_dir, expire=60) as spider:
        html = spider.get_html(
            "https://pypi.python.org/pypi/crawlib/", update_cache=False)
        html = spider.get_html(
            "https://pypi.python.org/pypi/crawlib/", ignore_cache=True)
        html = spider.get_html("https://pypi.python.org/pypi/crawlib/")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
