#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests
from fake_useragent import UserAgent
try:
    from .base import BaseSpider
    from ..decode import smart_decode
    from ..url_builder import util
except: # pragma: no cover
    from crawlib.spider.base import BaseSpider
    from crawlib.decode import smart_decode
    from crawlib.url_builder import util


class DownloadOversizeError(Exception):
    """
    The download target are not falls in the size range you specified.
    """


class Spider(BaseSpider):
    """

    """
    def __init__(self,
                 default_timeout=None,
                 default_headers=None,
                 default_wait_time=0.0):
        self.default_headers = default_headers
        self.default_timeout = default_timeout
        self.default_wait_time = default_wait_time
        self.domain_encoding_table = dict()

    def get_binary(self, url, params=None, headers=None, timeout=None,
                   wait_time=None, **kwargs):
        """
        Get binary data of an url.

        :param url: url you want to crawl.
        :param params: query params.
        :param headers: request headers.
        :param timeout: time out time in second.
        """
        headers = self.prepare_headers(headers)
        timeout = self.prepare_timeout(timeout)
        _ = self.prepare_wait_time(wait_time)

        if timeout:
            time.sleep(timeout)

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        binary = response.content
        return binary

    def get_html(self, url, params=None, headers=None, timeout=None,
                 encoding=None, errors="strict",
                 wait_time=None, **kwargs):
        """
        Get html source in text.

        :param encoding: if not given, the encoding will be auto-detected
        :param errors: options "ignore", "strict"; encoding error parameter
        """
        binary = self.get_binary(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )

        if encoding is None:
            domain = util.get_domain(url)
            if domain in self.domain_encoding_table:
                encoding = self.domain_encoding_table[domain]
                html = binary.decode(encoding, errors=errors)
            else:
                html, encoding, confidence = smart_decode(
                    binary, errors=errors)
                # cache domain name and encoding
                self.domain_encoding_table[domain] = encoding
        else:
            html = binary.decode(encoding, errors=errors)

        return html

    def download(self, url, dst, headers=None, timeout=None,
                 minimal_size=-1, maximum_size=1024**3,
                 wait_time=None, **kwargs):
        """
        Download binary content to destination.

        :param url: binary content url
        :param dst: path to the 'save_as' file
        :param timeout: time out time in second
        :param minimal_size: default -1, if response content smaller than
          minimal_size, then delete what just download.
        :param maximum_size: default 1GB, if response content greater than
          maximum_size, then delete what just download.
        """
        headers = self.prepare_headers(headers)
        timeout = self.prepare_timeout(timeout)
        _ = self.prepare_wait_time(wait_time)

        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            stream=True,
            **kwargs
        )

        chunk_size = 1024 * 1024
        downloaded_size = 0

        with open(dst, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if not chunk:
                    break
                f.write(chunk)
                downloaded_size += chunk_size

        if (downloaded_size < minimal_size) or (downloaded_size > maximum_size):
            try:
                os.remove(dst)
            except:
                pass
            msg = "resource at %s's size doesn't fall into (%s, %s) KB!" % (
                url, minimal_size, maximum_size,
            )
            raise DownloadOversizeError(msg)

