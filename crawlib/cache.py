#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A disk cache layer to store url and its html.
"""

from __future__ import print_function

import sys
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
        if value_type_is_binary is True:
            self._decompress = self._decompress_return_bytes
            self._compress = self._compress_bytes
        elif value_type_is_binary is False:
            self._decompress = self._decompress_return_str
            self._compress = self._compress_str
        else:
            msg = "`value_type_is_binary` arg has to be a boolean value!"
            raise ValueError(msg)
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


class CacheBackedDownloader(object):
    """
    Implement a disk cache backed url content downloader functionality.

    :param cache_dir: str, diskCache directory.
    :param read_cache_first: bool, If true, downloader will try read binary
        content from cache.
    :param alert_when_cache_missing: bool, If true, a log message will be
        displayed when url has not been seen in cache.
    :param always_update_cache: bool, If true, the response content will be
        saved to cache anyway.
    :param cache_expire: int, number seconds to expire.
    :param cache_value_type_is_binary: bool
    :param cache_compress_level: compress level, 1-9. 9 is highest.
    """

    def __init__(self,
                 cache_dir=None,
                 read_cache_first=False,
                 alert_when_cache_missing=False,
                 always_update_cache=False,
                 cache_expire=None,
                 cache_value_type_is_binary=None,
                 cache_compress_level=6,
                 **kwargs):

        self.cache_dir = cache_dir
        self.read_cache_first = read_cache_first
        self.alert_when_cache_missing = alert_when_cache_missing
        self.always_update_cache = always_update_cache
        self.cache_expire = cache_expire
        self.cache_value_type_is_binary = cache_value_type_is_binary

        # cache
        if (read_cache_first is True) and (cache_dir is None):
            raise ValueError(
                "Please specify the `cache_dir` to read response from cache!")
        if (read_cache_first is False) and (alert_when_cache_missing is True):
            raise ValueError(
                "Please turn on `read_cache_first = True` to enable alert when cache missing!")
        if (always_update_cache is True) and (cache_dir is None):
            raise ValueError(
                "Please specify the `cache_dir` to save response to cache!")
        if cache_dir:
            self.cache = create_cache(
                cache_dir,
                compress_level=cache_compress_level,
                value_type_is_binary=cache_value_type_is_binary,
            )

    def close_cache(self):
        if self.cache_dir is not None:
            self.cache.close()

    def try_read_cache(self, url):
        cache_consumed = False
        value = None
        if self.read_cache_first:
            if url in self.cache:
                value = self.cache[url]
                cache_consumed = True
            else:  # pragma: no cover
                if self.alert_when_cache_missing:
                    msg = "\n{} doesn't hit cache!".format(url)
                    sys.stdout.write(msg)
        return cache_consumed, value

    def should_we_update_cache(self,
                               any_type_response,
                               cache_cb,
                               cache_consumed_flag):
        """

        :param any_type_response: any response object.
        :param cache_cb: a call back function taking ``any_type_response``
            as input, and return a boolean value to indicate that whether we
            should update cache.
        :return: bool.

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
            return cache_cb(any_type_response)
