#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
url content downloader middleware using ``selenium``.
"""

from __future__ import unicode_literals
from selenium import webdriver

from ..util import add_params
from ..cache import CacheBackedDownloader
from .base_downloader import DownloaderABC


class BaseSeleliumDownloader(DownloaderABC, CacheBackedDownloader):
    """
    Implements common behavior for downloading url content.

    .. note::

        In ``__init__(self, ...)`` method, we only save the parameters.
        The actually webdriver creation happened in
        :meth:`BaseSeleliumDownloader.create_driver`.

    :param testmode: bool, see :meth:`BaseSeleniumDownloader.use_testmode`.
    """

    def __init__(self,
                 init_driver_func=lambda driver: driver,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 testmode=False,
                 **kwargs):
        self.driver = None

        self.init_driver_func = init_driver_func
        self.cache_dir = cache_dir
        self.read_cache_first = read_cache_first
        self.alert_when_cache_missing = alert_when_cache_missing
        self.always_update_cache = always_update_cache
        self.cache_expire = cache_expire
        self.testmode = testmode

        # in testmode we dont't create webdriver object instantly
        if self.testmode:
            self.use_testmode()
        else:
            self._create_driver()

        super(BaseSeleliumDownloader, self).__init__(
            cache_dir=self.cache_dir,
            read_cache_first=self.read_cache_first,
            alert_when_cache_missing=self.alert_when_cache_missing,
            always_update_cache=self.always_update_cache,
            cache_expire=self.cache_expire,
            cache_value_type_is_binary=False,
            cache_compress_level=6,
        )

    def use_testmode(self):
        """

        **中文文档**

        在测试中我们会有特殊的需求. 我们希望能用Selenium从测试Url上抓取Html, 然后对
        ``html_parser`` 中的函数进行测试. 期间我们希望能对Html进行缓存, 在短时间内重复
        运行测试时, 使用缓存中的Html. 当且仅当我们需要时, 才启动浏览器进行抓取. 这种
        模式我们称之为 ``测试模式`` (``testmode``).

        测试模式: 在测试模式中, 我们设定:

        1. 在未遭遇缓存未命中之前, 并不真正的创建 ``WebDriver`` 对象 (并不打开浏览器)
            只有在未命中时, 再创建并初始化 :attr:`BaseSeleliumDownloader.driver`.
        2. 永远先尝试从缓存中读取数据.
        3. 当缓存未命中时显示提示信息.
        4. 永远自动更新缓存.
        """
        self.read_cache_first = True
        self.alert_when_cache_missing = True
        self.always_update_cache = True

    def _create_driver(self, **kwargs):
        """
        Create webdriver, assign it to ``self.driver``, and run webdriver
        initiation process, which is usually used for manual login.
        """
        if self.driver is None:
            self.driver = self.create_driver(**kwargs)
            self.init_driver_func(self.driver)

    def create_driver(self, **kwargs):
        """
        Create webdriver instance.
        """
        raise NotImplementedError

    def get_html(self,
                 url,
                 params=None,
                 cache_cb=None,
                 **kwargs):
        """
        Get html of an url.
        """
        url = add_params(url, params)
        cache_consumed, value = self.try_read_cache(url)
        if cache_consumed:
            html = value
        else:
            self._create_driver()
            self.driver.get(url)
            html = self.driver.page_source

        if self.should_we_update_cache(html, cache_cb, cache_consumed):
            self.cache.set(
                url, html,
                expire=kwargs.get("cache_expire", self.cache_expire),
            )
        return html

    def download(self, *args, **kwargs):
        """
        .. warning::

            NOT IMPLEMENTED! python selenium doesn't support file and image downloading.
        """
        msg = (
            "Selenium should not be used to download non-html content. "
            "For downloading image or files, find the resource url, "
            "and use requests library to download it."
        )
        raise NotImplementedError(msg)

    def close_drive(self):
        if self.driver is not None:
            self.driver.close()

    def close(self):
        self.close_cache()
        self.close_drive()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


class ChromeDownloader(BaseSeleliumDownloader):
    """
    Chrome browser url content downloader.
    """

    def __init__(self,
                 chromedriver_executable_path,
                 init_driver_func=lambda driver: driver,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 testmode=False,
                 **kwargs):
        self.chromedriver_executable_path = chromedriver_executable_path
        super(ChromeDownloader, self).__init__(
            init_driver_func=init_driver_func,
            cache_dir=cache_dir,
            read_cache_first=read_cache_first,
            alert_when_cache_missing=alert_when_cache_missing,
            always_update_cache=always_update_cache,
            cache_expire=cache_expire,
            testmode=testmode,
            **kwargs
        )

    def create_driver(self, **kwargs):
        return webdriver.Chrome(executable_path=self.chromedriver_executable_path)
