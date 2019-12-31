# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site.music.view import n_music, n_artist, n_genre
from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session
from crawlib.tests.dummy_site_crawler.sql_backend.s2_music import (
    Base,
    MusicPage,
    ArtistPage,
    GenrePage,
    RandomMusicPage,
)


def setup_module():
    Base.metadata.create_all(engine)

    session = Session()
    session.query(MusicPage).delete()
    session.query(ArtistPage).delete()
    session.query(GenrePage).delete()
    session.query(RandomMusicPage).delete()
    session.commit()
    session.close()


@pytest.mark.order1
def test_start_recursive_crawler():
    session = Session()
    assert session.query(RandomMusicPage).count() == 0
    assert session.query(MusicPage).count() == 0
    assert session.query(ArtistPage).count() == 0
    assert session.query(GenrePage).count() == 0

    RandomMusicPage.smart_insert(session, RandomMusicPage(id=1))

    repeat_times = 3
    for i in range(repeat_times):
        RandomMusicPage.start_recursive_crawler(
            detailed_log=False,
            get_unfinished_session=session,
            start_process_pr_kwargs={"engine": engine},
        )

    assert session.query(ArtistPage).count() == n_artist
    assert session.query(GenrePage).count() == n_genre
    assert session.query(MusicPage).count() == n_music


@pytest.mark.order2
def test_statistics():
    session = Session()
    RandomMusicPage.print_statistics(seconds=3600, session=session)
    session.close()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
