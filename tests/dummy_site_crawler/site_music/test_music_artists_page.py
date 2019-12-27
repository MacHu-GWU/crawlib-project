# -*- coding: utf-8 -*-

import pytest

from crawlib.cache import create_cache_here
from crawlib.cached_request import CachedRequest
from crawlib.tests.dummy_site_crawler.site.s2_music.entity_music import ArtistPage

cache = create_cache_here(__file__)
spider = CachedRequest(cache=cache, log_cache_miss=True, expire=24 * 3600)
spider.use_requests()


class TestArtistPage(object):
    def test_parse_response(self):
        artist_id = 5
        artist_page = ArtistPage(_id=artist_id)
        url = artist_page.build_url()
        html = spider.request_for_html(url)
        pres = artist_page.parse_response(url, request=None, response=None, html=html)
        assert len(pres.entity.musics) > 0
        assert len(pres.entity.musics) == len(pres.children)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
