# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from crawlib.middleware.url_builder.builder import BaseUrlBuilder


class PythonOrgUrlBuilder(BaseUrlBuilder):
    pass


url_builder = PythonOrgUrlBuilder(domain="https://www.python.org")


def test_join_all():
    assert url_builder.join_all("/a", "/b") == "https://www.python.org/a/b"


def test_add_params():
    with raises(ValueError):
        url_builder.add_params("www.google.com/q", {"q": "Python"})

    url = url_builder.add_params("https://www.python.org/q", {"version": "2.7"})
    assert url == "https://www.python.org/q?version=2.7"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
