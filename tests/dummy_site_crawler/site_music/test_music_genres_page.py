# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site_crawler.mongo_backend.s2_music import GenrePage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestGenrePage(object):
    def test_parse_response(self):
        genre_id = 5
        genre_page = GenrePage(_id=genre_id)
        url = genre_page.build_url()
        print(url)
        html = spider.request_for_html(url)
        pres = genre_page.parse_response(url, request=None, response=None, html=html)
        assert len(pres.entity.musics) > 0
        assert len(pres.entity.musics) == len(pres.children)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
