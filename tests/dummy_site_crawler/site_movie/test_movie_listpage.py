# -*- coding: utf-8 -*-

import pytest
from crawlib2.cache import create_cache_here
from crawlib2.cached_request import CachedRequest
from crawlib2.tests.dummy_site_crawler.site.s1_movie.entity_listpage import ListPage
from crawlib2.tests.dummy_site.movie.controller.view import n_movie_each_page

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
        assert pres.entity._id == page_num
        assert len(pres.children) == n_movie_each_page
        assert pres.children[0].movie_id == (page_num - 1) * n_movie_each_page + 1
        assert pres.children[-1].movie_id == page_num * n_movie_each_page


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
