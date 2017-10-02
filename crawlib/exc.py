#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exceptions.
"""

from requests import Timeout as TimeoutError
try:
    from .spider.requests_spider import DownloadOversizeError
    from .html_parser.parser import SoupError, CaptchaError, WrongHtmlError, ParseError
except:  # pragma: no cover
    from crawlib.spider.requests_spider import DownloadOversizeError
    from crawlib.html_parser.parser import SoupError, CaptchaError, WrongHtmlError, ParseError
