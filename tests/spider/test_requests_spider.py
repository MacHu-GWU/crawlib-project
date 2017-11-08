#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from crawlib.spider.requests_spider import (
    spider, DownloadOversizeError,
)
from crawlib.header_builder import Headers


def teardown_module(module):
    import os
    try:
        os.remove("www.python.org.html")
    except:
        pass


class TestRequestsSpider(object):
    def test_get_binary(self):
        binary = spider.get_binary("https://www.python.org/")

    def test_get_html(self):
        html1 = spider.get_html("https://www.python.org/")
        html2 = spider.get_html("https://www.python.org/", encoding="utf-8")
        html3 = spider.get_html("https://www.python.org/",
                                encoding="utf-8",
                                headers={
                                    Headers.UserAgent.KEY: Headers.UserAgent.chrome
                                },
                                wait_time=0.01,
                                timeout=10)
        assert html1 == html2 == html3

    def test_download(self):
        spider.download("https://www.python.org/", "www.python.org.html")

    def test_download_size_not_in_range(self):
        with raises(DownloadOversizeError):
            spider.download(
                "https://www.python.org/", "www.python.org.html",
                minimal_size=1000 ** 3,
            )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
