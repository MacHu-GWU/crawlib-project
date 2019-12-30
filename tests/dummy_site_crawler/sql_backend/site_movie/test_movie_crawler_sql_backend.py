# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site.movie.view import max_page_id, n_movie, n_movie_each_page
from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session
from crawlib.tests.dummy_site_crawler.sql_backend.s1_movie import (
    Base,
    HomePage,
    ListPage,
    MoviePage,
    MovieCoverImagePage,
)


def setup_module():
    Base.metadata.create_all(engine)

    session = Session()
    session.query(HomePage).delete()
    session.query(ListPage).delete()
    session.query(MoviePage).delete()
    session.commit()
    session.close()


def test():
    session = Session()
    assert session.query(HomePage).count() == 0
    assert session.query(ListPage).count() == 0
    assert session.query(MoviePage).count() == 0

    HomePage.smart_insert(session, HomePage(id=1))
    HomePage.start_recursive_crawler(
        detailed_log=True,
        get_unfinished_session=session,
        start_process_pr_kwargs={"engine": engine},
    )

    assert session.query(HomePage).count() == 1
    assert session.query(ListPage).count() == max_page_id
    assert session.query(MoviePage).count() == n_movie

    assert session.query(HomePage).one().to_dict()[HomePage.n_listpage.name] == max_page_id
    for listpage in session.query(ListPage):
        assert listpage.to_dict()[ListPage.n_movie.name] <= n_movie_each_page

    for moviepage in session.query(MoviePage):
        assert moviepage.to_dict()[MoviePage.title.name] == "Movie %s Title" % moviepage.to_dict()[MoviePage.id.name]

    assert session.query(MovieCoverImagePage).filter(MovieCoverImagePage.image_content != None).count() \
           == n_movie

    session.close()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
