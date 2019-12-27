# -*- coding: utf-8 -*-

import os
import shutil

import pytest

from crawlib.cache import create_cache

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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
