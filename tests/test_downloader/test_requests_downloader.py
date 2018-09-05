#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import shutil
import pytest
from pytest import raises
from pathlib_mate import Path
from crawlib.downloader.requests_downloader import (
    RequestsDownloader, DownloadOversizeError,
)

cache_dir = Path(__file__).change(new_basename=".cache").abspath
dl_dst = Path(__file__).change(new_basename="python.org.html").abspath


def reset():
    try:
        shutil.rmtree(cache_dir)
    except:
        pass

    try:
        os.remove(dl_dst)
    except:
        pass


def teardown_module(module):
    reset()


class TestRequestsDownloader(object):
    def test(self):
        reset()

        dl = RequestsDownloader(
            cache_dir=cache_dir,
            read_cache_first=False,
            cache_expire=24 * 3600,
            use_random_user_agent=True,
        )

        url = "https://www.python.org/"
        assert url not in dl.cache
        html = dl.get_html(url, cache_cb=lambda res: True)
        assert url in dl.cache
        assert dl.cache[url].decode("utf-8") == html

        dl.read_cache_first = True
        res = dl.get(url)
        assert res.status_code is None

        dl.read_cache_first = False
        dl.download(url, dl_dst, overwrite=True)

        with raises(DownloadOversizeError):
            dl.download(url, dl_dst, overwrite=True, maximum_size=1024)
        with raises(DownloadOversizeError):
            dl.download(url, dl_dst, overwrite=True,
                        stream=True, maximum_size=1024)

        dl.close()

    def test_alert_when_cache_missing(self):
        reset()

        dl = RequestsDownloader(
            use_session=True,
            cache_dir=cache_dir,
            read_cache_first=True,
            alert_when_cache_missing=True,
            always_update_cache=True,
            cache_expire=24 * 3600,
            use_random_user_agent=True,
        )

        url = "https://www.python.org/downloads/"
        assert url not in dl.cache
        html = dl.get_html(url, decoder_encoding="utf-8")
        assert url in dl.cache
        html = dl.get_html(url, decoder_encoding="utf-8")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
