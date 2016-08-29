#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exceptions.
"""

from requests import Timeout as TimeoutError
try:
    from .spider import NotDownloadError
except:
    from crawlib.spider import NotDownloadError