#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.7"
__short_description__ = "tool set for crawler project."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from . import exc
    from .url_builder import BaseUrlBuilder, util
    from .html_parser import ParseResult, BaseHtmlParser
    from .spider.requests_spider import (
        spider as requests_spider,
    )
    from .status import Status
    from .header_builder import Headers
except ImportError:  # pragma: no cover
    pass
