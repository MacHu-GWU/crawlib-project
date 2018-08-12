#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.17"
__short_description__ = "tool set for crawler project."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    import scrapy
    _has_scrapy = True
except:
    _has_scrapy = False

try:
    from . import exc, util
    from .cache import create_cache, CacheBackedSpider
    from .data_class import ExtendedItem, ParseResult, Field
    from .data_class import (
        OneToManyMongoEngineItem,
        OneToManyRdsItem,
    )
    from .decode import smart_decode, decoder
    from .header_builder import Headers
    from .status import Status, FINISHED_STATUS_CODE
    from .timestamp import epoch, x_seconds_before_now, x_seconds_after_now

    # subpackage
    from .html_parser import (
        BaseHtmlParser,
        soupify, access_binary, auto_decode_and_soupify
    )
    from .url_builder.builder import BaseUrlBuilder
    from .spider.requests_spider import (
        spider as requests_spider,
    )
    from .spider.selenium_spider import (
        ChromeSpider,
    )
    from .pipeline import mongodb, rds
except ImportError as e:  # pragma: no cover
    print(e)
    pass
