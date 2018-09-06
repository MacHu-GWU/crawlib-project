#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..decode import decoder


class DownloaderABC(object):
    def get_html(self,
                 url,
                 params=None,
                 cache_cb=None,
                 decoder_encoding=None,
                 decoder_errors=decoder.ErrorsHandle.strict,
                 **kwargs):
        raise NotImplementedError

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
        raise NotImplementedError
