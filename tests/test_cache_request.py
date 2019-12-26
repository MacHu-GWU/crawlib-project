# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestCachedRequest(object):
    def test(self):
        url = "https://www.python.org/"
        # https://www.python.org doesn't hit cache! should appear over and over again
        html = spider.request_for_html(url, cacheable_callback=lambda html: False)

        url = "https://www.python.org/about/"
        # https://www.python.org doesn't hit cache! should appear every 10 seconds
        html = spider.request_for_html(url, cache_expire=10)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
