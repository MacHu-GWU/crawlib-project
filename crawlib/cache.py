# -*- coding: utf-8 -*-

"""
A disk cache layer to store url and its html.
"""

from __future__ import print_function

import os
import zlib

import diskcache


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


def create_cache(directory,
                 compress_level=6,
                 value_type_is_binary=False,
                 **kwargs):
    """
    Create a html cache. Html string will be automatically compressed.

    :type directory: str
    :param directory: path for the cache directory.

    :type compress_level: int
    :param compress_level: 0 ~ 9, 9 is slowest and smallest.

    :type value_type_is_binary: bool
    :param value_type_is_binary: default False.

    :param kwargs: other arguments.

    :rtype: diskcache.Cache
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


def create_cache_here(this_file: str,
                      compress_level: int = 6,
                      value_type_is_binary: bool = False,
                      **kwargs) -> diskcache.Cache:
    """
    Create a disk cache at the current directory. Cache file will be stored at
    ``here/.cache`` dir.

    :param this_file: always __file__.
    :param compress_level: compress level 1 is minimal, 9 is maximum compression.
    :param value_type_is_binary: if True, the value expected to be binary.
        otherwise string.
    :param kwargs: additional keyword arguments
    :return: a ``diskcache.Cache`` object
    """
    return create_cache(
        directory=os.path.join(os.path.dirname(this_file), ".cache"),
        compress_level=compress_level,
        value_type_is_binary=value_type_is_binary,
        **kwargs
    )
