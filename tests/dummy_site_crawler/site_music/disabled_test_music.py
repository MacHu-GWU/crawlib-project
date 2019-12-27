# -*- coding: utf-8 -*-

import pytest
from crawlib2.tests.dummy_site_crawler.db import client, db
from crawlib2.tests.dummy_site_crawler.site.s2_music import (
    RandomMusicPage,
    ArtistPage,
    GenrePage,
    MusicPage,
)
from crawlib2.tests.dummy_site.music.controller.view import n_music, n_artist, n_genre


def test():
    RandomMusicPage(_id=1).save()
    assert RandomMusicPage.col().find().count() == 1
    assert ArtistPage.col().find().count() == 0
    assert GenrePage.col().find().count() == 0
    assert MusicPage.col().find().count() == 0

    RandomMusicPage.start_all()
    RandomMusicPage.start_all()
    RandomMusicPage.start_all()

    assert ArtistPage.col().find().count() == n_artist
    assert GenrePage.col().find().count() == n_genre
    assert MusicPage.col().find().count() == n_music


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
