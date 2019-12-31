# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site.music.view import (
    max_n_artist, max_n_genre, n_random_music,
)
from crawlib.tests.dummy_site_crawler.sql_backend.s2_music import (
    MusicPage, ArtistPage, GenrePage, RandomMusicPage
)

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestMusicPage(object):
    def test_parse_response(self):
        music_id = 20
        music = MusicPage(id=music_id)
        url = music.build_url()
        html = spider.request_for_html(url)
        pres = music.parse_response(url, request=None, response=None, html=html)
        assert pres.entity_data["title"] == "Music {} Title".format(music_id)
        assert len(pres.children) == (max_n_artist + max_n_genre)


class TestArtistPage(object):
    def test_parse_response(self):
        artist_id = 5
        artist_page = ArtistPage(id=artist_id)
        url = artist_page.build_url()
        html = spider.request_for_html(url)
        pres = artist_page.parse_response(url, request=None, response=None, html=html)
        assert len(pres.entity_data["musics"]) > 0
        assert len(pres.entity_data["musics"]) == len(pres.children)


class TestGenrePage(object):
    def test_parse_response(self):
        genre_id = 5
        genre_page = GenrePage(id=genre_id)
        url = genre_page.build_url()
        html = spider.request_for_html(url)
        pres = genre_page.parse_response(url, request=None, response=None, html=html)
        assert len(pres.entity_data["musics"]) > 0
        assert len(pres.entity_data["musics"]) == len(pres.children)


class TestHomePage(object):
    def test_parse_response(self):
        rand_music_page = RandomMusicPage()
        url = rand_music_page.build_url()
        html = spider.request_for_html(url)
        pres = rand_music_page.parse_response(url, request=None, response=None, html=html)
        assert len(pres.entity_data["musics"]) == n_random_music
        assert len(pres.entity_data["musics"]) == len(pres.children)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
