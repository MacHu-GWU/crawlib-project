# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site.music.view import (
    n_artist,
    n_genre,
    n_music,
)
from crawlib.tests.dummy_site_crawler.mongo_backend.db import db
from crawlib.tests.dummy_site_crawler.mongo_backend.s2_music import (
    RandomMusicPage,
    ArtistPage,
    GenrePage,
    MusicPage,
)

_ = db


def setup_module():
    RandomMusicPage.col().delete_many({})
    ArtistPage.col().delete_many({})
    GenrePage.col().delete_many({})
    MusicPage.col().delete_many({})


@pytest.mark.order1
def test_start_recursive_crawler():
    assert RandomMusicPage.col().find().count() == 0
    assert ArtistPage.col().find().count() == 0
    assert GenrePage.col().find().count() == 0
    assert MusicPage.col().find().count() == 0

    RandomMusicPage(_id=1).save()
    repeat_times = 3
    for _ in range(repeat_times):
        RandomMusicPage.start_recursive_crawler(detailed_log=True, debug_mode=True)

    assert ArtistPage.col().find().count() == n_artist
    assert GenrePage.col().find().count() == n_genre
    assert MusicPage.col().find().count() == n_music


@pytest.mark.order2
def test_statistics():
    RandomMusicPage.print_statistics(seconds=3600)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
