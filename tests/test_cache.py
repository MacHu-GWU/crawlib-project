#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from crawlib.cache import CacheBackedSpider

cache_dir = os.path.join(os.path.dirname(__file__), ".cache")


class Spider(CacheBackedSpider):
    def get_html(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            html = "Hello World" * 10000
            self.cache.set(url, html)
            return html


def test_CacheBackedSpider():
    with Spider(cache_dir, expire=60) as spider:
        html = spider.get_html("https://pypi.python.org/pypi/crawlib/")
        html = spider.get_html("https://pypi.python.org/pypi/crawlib/")
        html = spider.get_html("https://pypi.python.org/pypi/crawlib/")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
