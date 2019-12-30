# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site_crawler.mongo_backend.s2_music import (
    RandomMusicPage, )

RandomMusicPage.smart_insert(RandomMusicPage(_id=1))
RandomMusicPage.start_recursive_crawler()
