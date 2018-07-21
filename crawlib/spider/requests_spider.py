#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests

try:
    from .. import helper, util
    from .base import BaseSpider
    from ..decode import decoder
except:  # pragma: no cover
    from crawlib import helper, util
    from crawlib.spider.base import BaseSpider
    from crawlib.decode import decoder


class DownloadOversizeError(Exception):
    """
    The download target are not falls in the size range you specified.
    """


class Spider(BaseSpider):
    """
    A general http spider.
    """

    def __init__(self,
                 default_timeout=None,
                 default_headers=None,
                 default_wait_time=0.0):
        self.default_headers = default_headers
        self.default_timeout = default_timeout
        self.default_wait_time = default_wait_time
        self.domain_encoding_table = dict()

    def get(self,
            url,
            params=None,
            headers=None,
            timeout=None,
            wait_time=None,
            **kwargs):
        """
        Get request

        :param url: url you want to crawl.
        :param params: query params.
        :param headers: request headers.
        :param timeout: time out time in second.
        :param wait_time: wait time in second before doing real request.

        :return: requests.Request
        """
        headers = self.prepare_headers(headers)
        timeout = self.prepare_timeout(timeout)
        wait_time = self.prepare_wait_time(wait_time)
        if wait_time:  # pragma: no cover
            self.sleep(wait_time)

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        return response

    def get_binary(self, url, params=None, headers=None, timeout=None,
                   wait_time=None, **kwargs):
        """
        Get binary data of an url.
        """
        response = self.get(
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            wait_time=wait_time,
            **kwargs
        )
        binary = response.content
        return binary

    def get_html(self,
                 url,
                 params=None,
                 headers=None,
                 timeout=None,
                 encoding=None,
                 errors="strict",
                 wait_time=None,
                 **kwargs):
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
            wait_time=wait_time,
            **kwargs
        )
        html = decoder.decode(
            binary=binary,
            url=url,
            encoding=encoding,
            errors=errors,
        )
        return html

    def download(self, url, dst, headers=None, timeout=None,
                 minimal_size=-1, maximum_size=1024 ** 6,
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
        wait_time = self.prepare_wait_time(wait_time)

        if wait_time:  # pragma: no cover
            self.sleep(wait_time)

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
                helper.repr_data_size(minimal_size),
                helper.repr_data_size(maximum_size),
            )
            raise DownloadOversizeError(msg)


spider = Spider()
