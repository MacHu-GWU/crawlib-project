#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use diskcache to store url and its html. To avoid hit single url again and
again.
"""

import zlib
import diskcache


class CompressStringDisk(diskcache.Disk):  # pragma: no cover
    """
    Serialization Layer.

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
        data = super(CompressStringDisk, self).\
            fetch(mode, filename, value, read)
        if not read:
            data = zlib.decompress(data).decode("utf-8")
        return data


class CacheBackedSpider(object):
    """
    A disk cache backed spider.

    :param directory: where you gonna put cache file.
    :param compress_level: int. 0 ~ 9, 0 is fastest but no compression. 9 is
        slowest with highest compression.
    :param expire: seconds that the cache will be expired.
    """

    def __init__(self, directory, compress_level=6, expire=None):
        self.cache = diskcache.Cache(
            directory,
            disk=CompressStringDisk,
            disk_compress_level=compress_level,
        )
        self.expire = expire

    def close(self):
        self.cache.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_html(self, url, expire=None, ignore_cache=False, update_cache=True,
                 **kwargs):
        """
        Please implement this method.
        """
        raise NotImplementedError
