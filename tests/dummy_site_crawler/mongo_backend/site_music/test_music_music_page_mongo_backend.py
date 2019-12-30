# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site.music.view import (
    max_n_artist, max_n_genre,
)
from crawlib.tests.dummy_site_crawler.mongo_backend.s2_music import MusicPage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestMusicPage(object):
    def test_parse_response(self):
        music_id = 20
        music = MusicPage(_id=music_id)
        url = music.build_url()
        html = spider.request_for_html(url)
        pres = music.parse_response(url, request=None, response=None, html=html)
        assert pres.entity_data.title == "Music {} Title".format(music_id)
        assert len(pres.children) == (max_n_artist + max_n_genre)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
