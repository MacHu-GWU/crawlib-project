#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


def test():
    import crawlib

    crawlib.BaseUrlBuilder
    crawlib.ParseResult
    crawlib.BaseHtmlParser
    crawlib.util
    crawlib.Status
    crawlib.Headers

    exc = crawlib.exc
    exc.DownloadOversizeError
    exc.TimeoutError
    exc.SoupError
    exc.CaptchaError
    exc.WrongHtmlError
    exc.ParseError


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
