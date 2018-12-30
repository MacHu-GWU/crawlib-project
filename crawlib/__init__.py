#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.27"
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
except:  # pragma: no cover
    _has_scrapy = False

try:
    from . import exc, util
    from .cache import create_cache, CacheBackedDownloader
    from .data_class import ExtendedItem, ParseResult, Field
    from .data_class import (
        OneToManyMongoEngineItem,
        OneToManyRdsItem,
    )
    from .decode import smart_decode, decoder
    from .logger import SpiderLogger
    from .header_builder import Headers
    from .spider import execute_one_to_many_job
    from .status import Status, FINISHED_STATUS_CODE
    from .timestamp import epoch, x_seconds_before_now, x_seconds_after_now

    # subpackage
    from .downloader import (
        RequestsDownloader,
        ChromeDownloader,
    )
    from .html_parser import (
        BaseHtmlParser,
        soupify, access_binary, auto_decode_and_soupify,
    )
    from .url_builder.builder import BaseUrlBuilder
    from .pipeline import mongodb, rds
except ImportError as e:  # pragma: no cover
    print(e)
    pass
