#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exceptions.
"""

from requests import Timeout as TimeoutError
from .spider.requests_spider import DownloadOversizeError
from .html_parser.errors import (
    CaptchaError,
    ForbiddenError,
    WrongHtmlError,
    SoupError,
    ParseError,
    IncompleteDataError,
    ServerSideError,
)
