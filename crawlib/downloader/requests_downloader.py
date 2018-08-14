#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from ..header_builder import Headers
from ..cache import create_cache
from ..decode import url_specified_decoder
from ..helper import repr_data_size
from ..exc import DownloadOversizeError


class RequestsDownloader(object):
    def __init__(self,
                 use_session=False,
                 use_tor=False,
                 tor_port=9050,
                 cache_on=False,
                 cache_dir=None,
                 cache_expire=0,
                 random_user_agent=True,
                 **kwargs):
        # session and tor
        if (use_session is False) and (use_tor is True):
            raise ValueError

        if use_session is True:
            self.ses = requests.sessions()
        else:
            self.ses = requests

        if use_tor is True:
            self.proxies = {
                "http": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
                "https": "socks5h://localhost:{tor_port}".format(tor_port=tor_port),
            }

        # cache
        if (cache_on is True) and (cache_dir is None):
            raise ValueError("Please specify the `cache_dir`!")
        self.cache_on = cache_on
        if cache_on:
            self.cache = create_cache(
                cache_dir, value_type_is_binary=True)
        self.cache_expire = cache_expire

        #
        self.random_user_agent = random_user_agent

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

    def get(self,
            url,
            params=None,
            cache_cb=None,
            **kwargs):
        if self.random_user_agent:
            headers = kwargs.get("headers", dict())
            headers.update({Headers.UserAgent.KEY: Headers.UserAgent.random()})
            kwargs["headers"] = headers

        response = self.ses.get(url, params=params, **kwargs)
        if self._should_we_do_cache(response, cache_cb):
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
        response = self.get(
            url=url,
            params=params,
            cache_cb=cache_cb,
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

    def default_cache_cb(self, response):
        return False

    def _should_we_do_cache(self, response, cache_cb):
        if self.cache_on:
            if cache_cb is None:
                return True
            else:
                return cache_cb(response)
        else:
            return False
