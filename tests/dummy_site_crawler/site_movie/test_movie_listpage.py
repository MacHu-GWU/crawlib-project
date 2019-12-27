# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site.movie.view import n_movie_each_page
from crawlib.tests.dummy_site_crawler.site.s1_movie.entity_listpage import ListPage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestListPage(object):
    def test_parse_response(self):
        page_num = 3
        listpage = ListPage(_id=page_num)
        url = listpage.build_url()
        html = spider.request_for_html(url)
        pres = listpage.parse_response(url, request=None, response=None, html=html)
        assert len(pres.children) == n_movie_each_page


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
