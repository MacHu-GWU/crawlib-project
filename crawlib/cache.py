#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use diskcache to store url and its html. To avoid hit single url again and
again.
"""

import zlib
import requests
import diskcache

from . import exc
from .decode import decoder


class CompressStringDisk(diskcache.Disk):  # pragma: no cover
    """
    Serialization Layer. Value has to be bytes or string type, and will be
    compressed using zlib before stored to disk.

    - Key: str, url.
    - Value: str, html.
    """

    def __init__(self, directory, compress_level=6, **kwargs):
        self.compress_level = compress_level
        super(CompressStringDisk, self).__init__(directory, **kwargs)

    def get(self, key, raw):
        data = super(CompressStringDisk, self).get(key, raw)
        return zlib.decompress(data).decode("utf-8")

    def store(self, value, read):
        if not read:
            value = zlib.compress(value.encode("utf-8"), self.compress_level)
        return super(CompressStringDisk, self).store(value, read)

    def fetch(self, mode, filename, value, read):
        data = super(CompressStringDisk, self). \
            fetch(mode, filename, value, read)
        if not read:
            data = zlib.decompress(data).decode("utf-8")
        return data


def create_cache(directory, compress_level=6, **kwargs):
    cache = diskcache.Cache(
        directory,
        disk=CompressStringDisk,
        disk_compress_level=compress_level,
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

    def __init__(self, directory, compress_level=6, expire=None):
        self.cache = create_cache(directory, compress_level)
        self.expire = expire

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

        if ignore_cache:
            req = requests.get(url, **kwargs)
        else:
            if url in self.cache:
                return self.cache[url]
            else:
                req = requests.get(url, **kwargs)
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
