2# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site.movie.view import max_page_id
from crawlib.tests.dummy_site_crawler.mongo_backend.s1_movie import HomePage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestHomePage(object):
    def test_parse_response(self):
        homepage = HomePage()
        url = homepage.build_url()
        html = spider.request_for_html(url)
        pres = homepage.parse_response(url, request=None, response=None, html=html)
        assert pres.entity_data["max_page_num"] == max_page_id
        assert len(pres.children) == max_page_id
        assert pres.children[-1]._id == max_page_id


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
