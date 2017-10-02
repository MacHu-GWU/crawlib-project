#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from crawlib.url_builder import util


def test_get_netloc():
    assert util.get_netloc("https://www.python.org/doc/") == "www.python.org"


def test_get_domain():
    assert util.get_domain(
        "https://www.python.org/doc/") == "https://www.python.org"


def test_join_all():
    domain = "https://www.python.org/"
    assert util.join_all(domain, "a", "b") == "https://www.python.org/a/b"
    assert util.join_all(domain, "/a", "/b") == "https://www.python.org/a/b"
    assert util.join_all(domain, "a/", "b/") == "https://www.python.org/a/b"
    assert util.join_all(domain, "/a/", "/b/") == "https://www.python.org/a/b"
    assert util.join_all(domain, "a/b") == "https://www.python.org/a/b"
    assert util.join_all(domain, "/a/b/") == "https://www.python.org/a/b"
    assert util.join_all(domain, "") == "https://www.python.org"


def test_add_params():
    endpoint = "https://www.google.com/search"
    params = {"q": "python"}
    assert util.add_params(
        endpoint, params) == "https://www.google.com/search?q=python"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
