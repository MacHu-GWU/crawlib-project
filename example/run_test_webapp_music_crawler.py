# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site_crawler.db import db
from crawlib.tests.dummy_site_crawler.site.s2_music import (
    RandomMusicPage, MusicPage, ArtistPage, GenrePage,
)

RandomMusicPage.smart_insert(RandomMusicPage(_id=1))
RandomMusicPage.start_all()
