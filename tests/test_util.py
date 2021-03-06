# -*- coding: utf-8 -*-

import pytest
from crawlib import util


def test_get_netloc():
    assert util.get_netloc("https://www.python.org/doc/") == "www.python.org"


def test_get_domain():
    assert util.get_domain("https://www.python.org/doc/") == "https://www.python.org"
    with pytest.raises(ValueError):
        util.get_domain("www.python.org/doc/")


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
    assert util.add_params(endpoint, params) \
           == "https://www.google.com/search?q=python"
    assert util.add_params(endpoint, params=None) == endpoint

    params = [("year", 2000), ("month", 12), ("day", 31)]
    assert util.add_params(endpoint, params=params) \
           == "https://www.google.com/search?year=2000&month=12&day=31"


def test_get_all_subclass():
    class X: pass

    class A(X): pass

    class B(X): pass

    class C(A, B): pass

    class D(C): pass

    class E(C): pass

    assert util.get_all_subclass(X) == {A, B, C, D, E}


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
