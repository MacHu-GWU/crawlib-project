#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
downloader middleware using ``requests``.
"""

from __future__ import unicode_literals
import os
import requests
import sys
from atomicwrites import atomic_write
from six import PY2
from ..util import add_params
from ..header_builder import Headers
from ..cache import CacheBackedDownloader
from ..decode import url_specified_decoder
from ..helper import repr_data_size
from ..exc import DownloadOversizeError
from .base_downloader import DownloaderABC


class RequestsDownloader(DownloaderABC, CacheBackedDownloader):
    """
    Rich feature downloader for making http request.

    :param use_session: bool, whether you use session to communicate.
    :param use_tor: bool, whether you use tor network. For information
        about installation for tor, see
        https://www.torproject.org/docs/tor-doc-osx.html.en
    :param tor_port: int, By default, is 9050.
    :param cache_dir: str, diskCache directory.
    :param read_cache_first: bool, If true, downloader will try read binary
        content from cache.
    :param alert_when_cache_missing: bool, If true, a log message will be
        displayed when url has not been seen in cache.
    :param always_update_cache: bool, If true, the response content will be
        saved to cache anyway.
    :param cache_expire: int, number seconds to expire.
    :param use_random_user_agent: bool, if true, a random user agent will be
        used for http request.
    """

    def __init__(self,
                 use_session=False,
                 use_tor=False,
                 tor_port=9050,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 use_random_user_agent=True,
                 **kwargs):
        self.use_session = use_session
        self.use_tor = use_tor
        self.tor_port = 9050

        self.use_random_user_agent = use_random_user_agent

        # session and tor
        if (use_session is False) and (use_tor is True):
            raise ValueError(
                "You have to use session when you want to use tor.")

        if use_session is True:
            self.ses = requests.Session()
        else:
            self.ses = requests

        if use_tor is True:  # pragma: no cover
            self.ses.proxies = {
                "http": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
                "https": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
            }

        super(RequestsDownloader, self).__init__(
            cache_dir=cache_dir,
            read_cache_first=read_cache_first,
            alert_when_cache_missing=alert_when_cache_missing,
            always_update_cache=always_update_cache,
            cache_expire=cache_expire,
            cache_value_type_is_binary=True,
            cache_compress_level=6,
        )

    def close_session(self):
        try:
            self.ses.close()
        except:
            pass

    def close(self):
        self.close_cache()
        self.close_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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

        cache_consumed, value = self.try_read_cache(url)
        if cache_consumed:
            response = requests.Response()
            response.url = url
            response._content = value
        else:
            response = self.ses.get(url, **kwargs)

        if self.should_we_update_cache(response, cache_cb, cache_consumed):
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
                 decoder_errors=url_specified_decoder.ErrorsHandle.strict,
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

    def raise_download_oversize_error(self,
                                      url,
                                      downloaded_size,
                                      minimal_size,
                                      maximum_size):
        msg = "resource at %s's size is %s, doesn't fall into %s to %s!" % (
            url,
            repr_data_size(downloaded_size),
            repr_data_size(minimal_size),
            repr_data_size(maximum_size),
        )
        raise DownloadOversizeError(msg)

    def download(self,
                 url,
                 dst,
                 params=None,
                 cache_cb=None,
                 overwrite=False,
                 stream=False,
                 minimal_size=-1,
                 maximum_size=1024 ** 6,
                 **kwargs):
        """
        Download binary content to destination.

        :param url: binary content url
        :param dst: path to the 'save_as' file
        :param cache_cb: (optional) a function that taking requests.Response
            as input, and returns a bool flag, indicate whether should update the cache.
        :param overwrite: bool,
        :param stream: bool, whether we load everything into memory at once, or read
            the data chunk by chunk
        :param minimal_size: default -1, if response content smaller than
          minimal_size, then delete what just download.
        :param maximum_size: default 1GB, if response content greater than
          maximum_size, then delete what just download.
        """
        response = self.get(
            url,
            params=params,
            cache_cb=cache_cb,
            stream=stream,
            **kwargs
        )

        if not overwrite:
            if os.path.exists(dst):
                raise OSError("'%s' exists!" % dst)

        if stream:
            chunk_size = 1024 * 1024
            downloaded_size = 0
            with atomic_write(dst, mode="wb") as f:
                for chunk in response.iter_content(chunk_size):
                    if not chunk:  # pragma: no cover
                        break
                    f.write(chunk)
                    downloaded_size += chunk_size
                if (downloaded_size < minimal_size) or (downloaded_size > maximum_size):
                    self.raise_download_oversize_error(
                        url, downloaded_size, minimal_size, maximum_size)
        else:
            content = response.content
            downloaded_size = sys.getsizeof(content)
            if (downloaded_size < minimal_size) or (downloaded_size > maximum_size):
                self.raise_download_oversize_error(
                    url, downloaded_size, minimal_size, maximum_size)
            else:
                with atomic_write(dst, mode="wb") as f:
                    f.write(content)

    def cache_cb_status_code_2xx(self, response):  # pragma: no cover
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
