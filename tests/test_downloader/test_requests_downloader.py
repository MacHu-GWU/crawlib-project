#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import pytest
from pathlib_mate import Path
from crawlib import create_cache
from crawlib.downloader.requests_downloader import RequestsDownloader

cache_dir = Path(__file__).change(new_basename=".cache").abspath
cache = create_cache(cache_dir)

dl = RequestsDownloader(
    cache_on=True,
    cache_dir=cache_dir,
    cache_expire=24 * 3600,
    random_user_agent=True,
)

dl_dst = Path(__file__).change(new_basename="python.org.html").abspath


def teardown_module(module):
    try:
        os.remove(dl_dst)
    except:
        pass


class TestRequestsDownloader(object):
    def test(self):
        url = "https://www.python.org/"
        html = dl.get_html(url)
        assert dl.cache[url].decode("utf-8") == html

        dl.download(url, dl_dst)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
