#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from six import PY2
from selenium import webdriver

from ..util import add_params
from ..cache import CacheBackedDownloader
from .base_downloader import DownloaderABC


class BaseSeleliumSpider(DownloaderABC, CacheBackedDownloader):
    def __init__(self,
                 driver=None,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 **kwargs):
        self.driver = driver
        self.cache_dir = cache_dir
        self.read_cache_first = read_cache_first
        self.alert_when_cache_missing = alert_when_cache_missing
        self.always_update_cache = always_update_cache
        self.cache_expire = cache_expire

        super(BaseSeleliumSpider, self).__init__(
            cache_dir=cache_dir,
            read_cache_first=read_cache_first,
            alert_when_cache_missing=alert_when_cache_missing,
            always_update_cache=always_update_cache,
            cache_expire=cache_expire,
            cache_value_type_is_binary=False,
            cache_compress_level=6,
        )

    def get_html(self,
                 url,
                 params=None,
                 cache_cb=None,
                 **kwargs):
        """
        Get html of an url.
        """
        url = add_params(url, params)
        if PY2:
            url = unicode(url)

        cache_consumed, value = self.try_read_cache(url)
        if cache_consumed:
            html = value
        else:
            self.driver.get(url)
            html = self.driver.page_source

        if self.should_we_update_cache(html, cache_cb, cache_consumed):
            self.cache.set(
                url, html,
                expire=kwargs.get("cache_expire", self.cache_expire),
            )
        return html

    def download(self, *args, **kwargs):
        msg = (
            "Selenium should not be used to download non-html content. "
            "For downloading image or files, find the resource url, "
            "and use requests library to download it."
        )
        raise NotImplementedError(msg)

    def close_drive(self):
        self.driver.close()

    def close(self):
        self.close_cache()
        self.close_drive()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


class ChromeDownloader(BaseSeleliumSpider):
    def __init__(self,
                 chromedriver_executable_path,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 **kwargs):
        driver = webdriver.Chrome(executable_path=chromedriver_executable_path)
        super(ChromeDownloader, self).__init__(
            driver=driver,
            cache_dir=cache_dir,
            read_cache_first=read_cache_first,
            alert_when_cache_missing=alert_when_cache_missing,
            always_update_cache=always_update_cache,
            cache_expire=cache_expire,
            **kwargs
        )
