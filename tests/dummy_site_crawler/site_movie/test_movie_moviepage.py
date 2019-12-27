# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site_crawler.site.s1_movie.entity_movie import MoviePage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestMoviePage(object):
    def test_parse_response(self):
        movie_id = 25
        movie = MoviePage(_id=movie_id)
        url = movie.build_url()
        html = spider.request_for_html(url)
        pres = movie.parse_response(url, request=None, response=None, html=html)
        assert pres.entity.title == "Movie {} Title".format(movie_id)
        assert len(pres.children) == 0


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
