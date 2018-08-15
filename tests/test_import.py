#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


def test():
    import crawlib

    crawlib.RequestsDownloader
    crawlib.BaseUrlBuilder
    crawlib.BaseHtmlParser

    crawlib.ExtendedItem
    crawlib.OneToManyRdsItem
    crawlib.OneToManyRdsItem
    crawlib.ParseResult

    crawlib.util
    crawlib.Status
    crawlib.Headers

    crawlib.create_cache
    crawlib.CacheBackedSpider

    exc = crawlib.exc
    exc.DownloadOversizeError
    exc.TimeoutError
    exc.SoupError
    exc.CaptchaError
    exc.WrongHtmlError
    exc.ParseError
    exc.DecodeError


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
