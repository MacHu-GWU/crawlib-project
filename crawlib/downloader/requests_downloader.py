#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
downloader middleware using ``requests``.
"""

from __future__ import unicode_literals
import os
import requests
from six import PY2
from ..util import add_params
from ..header_builder import Headers
from ..cache import create_cache
from ..decode import url_specified_decoder
from ..helper import repr_data_size
from ..exc import DownloadOversizeError


class RequestsDownloader(object):
    """

    """

    def __init__(self,
                 use_session=False,
                 use_tor=False,
                 tor_port=9050,
                 cache_dir=None,
                 read_cache_first=False,
                 always_update_cache=False,
                 cache_expire=None,
                 use_random_user_agent=True,
                 **kwargs):
        self.use_session = use_session
        self.use_tor = use_tor
        self.tor_port = 9050
        self.cache_dir = cache_dir
        self.read_cache_first = read_cache_first
        self.always_update_cache = always_update_cache
        self.cache_expire = cache_expire
        self.use_random_user_agent = use_random_user_agent

        # session and tor
        if (use_session is False) and (use_tor is True):
            raise ValueError("You have to use session when you want to use tor.")

        if use_session is True:
            self.ses = requests.Sessions()
        else:
            self.ses = requests

        if use_tor is True:
            self.ses.proxies = {
                "http": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
                "https": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
            }

        # cache
        if (read_cache_first is True) and (cache_dir is None):
            raise ValueError("Please specify the `cache_dir` to read response from cache!")
        if (always_update_cache is True) and (cache_dir is None):
            raise ValueError("Please specify the `cache_dir` to save response to cache!")
        if cache_dir:
            self.cache = create_cache(cache_dir, value_type_is_binary=True)
        self.cache_expire = cache_expire

    def close(self):
        try:
            self.cache.close()
        except:
            pass

        try:
            self.ses.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def read_cache(self, url):
        pass

    def get(self,
            url,
            params=None,
            cache_cb=None,
            **kwargs):
        """
        Make http get request.

        :param url:
        :param params:
        :param cache_cb: (optional) a function that taking requests.Response
            as input, and returns a bool flag, indicate whether should update the cache.
        :param cache_expire: (optional).
        :param kwargs: optional arguments.
        """
        if self.use_random_user_agent:
            headers = kwargs.get("headers", dict())
            headers.update({Headers.UserAgent.KEY: Headers.UserAgent.random()})
            kwargs["headers"] = headers

        url = add_params(url, params)
        if PY2:
            url = unicode(url)

        _cache_comsumted = False
        if self.read_cache_first:
            if url in self.cache:
                response = requests.Response()
                response.url = url
                response._content = self.cache[url]
                _cache_comsumted = True

        if _cache_comsumted is False:
            response = self.ses.get(url, **kwargs)

        if self._should_we_update_cache(response, cache_cb, _cache_comsumted):
            self.cache.set(
                url, response.content,
                expire=kwargs.get("cache_expire", self.cache_expire),
            )
        return response

    def get_html(self,
                 url,
                 params=None,
                 cache_cb=None,
                 decoder_encoding=None,
                 decoder_errors="strict",
                 **kwargs):
        """
        Get html of an url.
        """
        response = self.get(
            url=url,
            params=params,
            cache_cb=cache_cb,
            **kwargs
        )
        return url_specified_decoder.decode(
            binary=response.content,
            url=response.url,
            encoding=decoder_encoding,
            errors=decoder_errors,
        )

    def download(self,
                 url,
                 dst,
                 params=None,
                 cache_cb=None,
                 minimal_size=-1,
                 maximum_size=1024 ** 6,
                 **kwargs):
        """
        Download binary content to destination.

        :param url: binary content url
        :param dst: path to the 'save_as' file
        :param minimal_size: default -1, if response content smaller than
          minimal_size, then delete what just download.
        :param maximum_size: default 1GB, if response content greater than
          maximum_size, then delete what just download.
        """
        response = self.get(
            url,
            params=params,
            cache_cb=cache_cb,
            **kwargs
        )

        chunk_size = 1024 * 1024
        downloaded_size = 0

        with open(dst, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if not chunk:  # pragma: no cover
                    break
                f.write(chunk)
                downloaded_size += chunk_size

        if (downloaded_size < minimal_size) or (downloaded_size > maximum_size):
            try:
                os.remove(dst)
            except:  # pragma: no cover
                pass
            msg = "resource at %s's size doesn't fall into %s to %s!" % (
                url,
                repr_data_size(minimal_size),
                repr_data_size(maximum_size),
            )
            raise DownloadOversizeError(msg)

    def _should_we_update_cache(self, response, cache_cb, cache_consumed_flag):
        """

        :param response:
        :param cache_cb:
        :return:

        **中文文档**

        1. 如果 ``cache_consumed_flag`` 为 True, 那么说明已经从cache中读取过数据了,
            再存也没有意义.
        2. 如果 ``self.always_update_cache`` 为 True, 那么强制更新cache. 我们不用担心
            发生已经读取过cache, 然后再强制更新的情况, 因为之前我们已经检查过
            ``cache_consumed_flag`` 了.
        3. 如果没有指定 ``cache_cb`` 函数, 那么默认不更新cache.
        """
        if cache_consumed_flag:
            return False

        if self.always_update_cache:
            return True

        if cache_cb is None:
            return False
        else:
            return cache_cb(response)

    def cache_cb_status_code_2xx(self, response):
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
