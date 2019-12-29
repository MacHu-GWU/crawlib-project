# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site.movie.view import n_movie_each_page, max_page_id
from crawlib.tests.dummy_site_crawler.sql_backend.s1_movie import (
    MovieCoverImagePage, MoviePage, ListPage, HomePage,
)

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestMovieCoverImagePage(object):
    def test_parse_response(self):
        movie_id = 25
        movie_cover_image = MovieCoverImagePage(id=movie_id)
        url = movie_cover_image.build_url()
        html = spider.request_for_html(url)
        pres = movie_cover_image.parse_response(url, request=None, response=None, html=html)

        assert "<div" in pres.entity.image_content
        assert len(pres.children) == 0


class TestMoviePage(object):
    def test_parse_response(self):
        movie_id = 25
        movie = MoviePage(id=movie_id)
        url = movie.build_url()
        html = spider.request_for_html(url)
        pres = movie.parse_response(url, request=None, response=None, html=html)
        assert pres.entity.title == "Movie {} Title".format(movie_id)
        assert len(pres.children) == 0


class TestListPage(object):
    def test_parse_response(self):
        page_num = 3
        listpage = ListPage(id=page_num)
        url = listpage.build_url()
        html = spider.request_for_html(url)
        pres = listpage.parse_response(url, request=None, response=None, html=html)
        assert len(pres.children) == n_movie_each_page


class TestHomePage(object):
    def test_parse_response(self):
        homepage = HomePage()
        url = homepage.build_url()
        html = spider.request_for_html(url)
        pres = homepage.parse_response(url, request=None, response=None, html=html)
        assert pres.entity.max_page_num == max_page_id
        assert len(pres.children) == max_page_id
        assert pres.children[-1].id == max_page_id


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
