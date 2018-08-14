#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A disk cache layer to store url and its html.
"""

from __future__ import print_function

import zlib
import requests
import diskcache

from . import exc
from .decode import decoder


class CompressedDisk(diskcache.Disk):  # pragma: no cover
    """
    Serialization Layer. Value has to be bytes or string type, and will be
    compressed using zlib before stored to disk.

    - Key: str, url.
    - Value: str or bytes, html or binary content.
    """

    def __init__(self,
                 directory,
                 compress_level=6,
                 value_type_is_binary=False,
                 **kwargs):
        self.compress_level = compress_level
        self.value_type_is_binary = value_type_is_binary
        if value_type_is_binary:
            self._decompress = self._decompress_return_bytes
            self._compress = self._compress_bytes
        else:
            self._decompress = self._decompress_return_str
            self._compress = self._compress_str
        super(CompressedDisk, self).__init__(directory, **kwargs)

    def _decompress_return_str(self, data):
        return zlib.decompress(data).decode("utf-8")

    def _decompress_return_bytes(self, data):
        return zlib.decompress(data)

    def _compress_str(self, data):
        return zlib.compress(data.encode("utf-8"), self.compress_level)

    def _compress_bytes(self, data):
        return zlib.compress(data, self.compress_level)

    def get(self, key, raw):
        data = super(CompressedDisk, self).get(key, raw)
        return self._decompress(data)

    def store(self, value, read, **kwargs):
        if not read:
            value = self._compress(value)
        return super(CompressedDisk, self).store(value, read, **kwargs)

    def fetch(self, mode, filename, value, read):
        data = super(CompressedDisk, self). \
            fetch(mode, filename, value, read)
        if not read:
            data = self._decompress(data)
        return data


def create_cache(directory, compress_level=6, value_type_is_binary=False, **kwargs):
    """
    Create a html cache. Html string will be automatically compressed.

    :param directory: path for the cache directory.
    :param compress_level: 0 ~ 9, 9 is slowest and smallest.
    :param kwargs: other arguments.
    :return: a `diskcache.Cache()`
    """
    cache = diskcache.Cache(
        directory,
        disk=CompressedDisk,
        disk_compress_level=compress_level,
        disk_value_type_is_binary=value_type_is_binary,
        **kwargs
    )
    return cache


class CacheBackedSpider(object):
    """
    A disk cache backed spider.

    :param directory: where you gonna put cache file.
    :param compress_level: int. 0 ~ 9, 0 is fastest but no compression. 9 is
        slowest with highest compression.
    :param expire: seconds that the cache will be expired.
    """

    def __init__(self,
                 directory,
                 compress_level=6,
                 expire=None,
                 cache_miss_warning=True):
        self.cache = create_cache(directory, compress_level)
        self.expire = expire
        self.cache_miss_warning = cache_miss_warning

    def close(self):
        self.cache.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_html(self,
                 url,
                 encoding=None,
                 decode_errors="ignore",
                 expire=None,
                 ignore_cache=False,
                 update_cache=True,
                 **kwargs):
        """
        Get html from url endpoint, if it is in cache, use cached html.

        :param url: url endpoing.
        :param encoding: html charset for decoding.
        :param decode_errors: how do you want to handle decode error,
            one of 'strict', 'ignore' and 'replace'.
        :param expire: seconds until item expires.
        :param ignore_cache: if ``True``, then hit the real website anyway.
        :param update_cache: by default, the html will be cached only if
            200 ~ 299 status code is returned. But, if ``False``,
            then it will not be cached.
        """
        if expire is None:
            expire = self.expire

        cache_missed = False
        if ignore_cache:
            req = requests.get(url, **kwargs)
        else:
            if url in self.cache:
                return self.cache[url]
            else:
                cache_missed = True
                req = requests.get(url, **kwargs)

        if cache_missed:
            if self.cache_miss_warning:
                msg = "Cache miss warn: {} doesn't hit cache!".format(url)
                print(msg)

        if 200 <= req.status_code < 300:
            html = decoder.decode(
                binary=req.content,
                url=url,
                encoding=encoding,
                errors=decode_errors,
            )
            if update_cache:
                self.cache.set(url, html, expire=expire)
            return html
        else:  # pragma: no cover
            raise exc.WrongHtmlError(url)
