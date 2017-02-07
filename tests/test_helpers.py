#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib.helpers import url_join


def test_url_join():
    domain = "https://www.python.org"
    assert url_join(domain, "a", "b") == "https://www.python.org/a/b"
    assert url_join(domain, "/a", "/b") == "https://www.python.org/a/b"
    assert url_join(domain, "a/", "b/") == "https://www.python.org/a/b"
    assert url_join(domain, "/a/", "/b/") == "https://www.python.org/a/b"
        

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])