# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session
from crawlib.tests.dummy_site_crawler.sql_backend.s1_movie import (
    Base,
    HomePage,
    ListPage,
    MoviePage,
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
    HomePage.start_all(
        detailed_log=True,
        get_unfinished_session=session,
        start_process_pr_kwargs={"engine": engine},
    )
    #
    # assert HomePage.col().find().count() == 1
    # assert ListPage.col().find().count() == max_page_id
    # assert MoviePage.col().find().count() == n_movie
    #
    # assert HomePage.col().find_one()[HomePage.n_listpage.name] == max_page_id
    # for doc in ListPage.col().find():
    #     assert doc[ListPage.n_movie.name] <= n_movie_each_page
    #
    # for doc in MoviePage.col().find():
    #     assert doc[MoviePage.title.name] == "Movie %s Title" % doc[MoviePage._id.name]
    #
    # assert MovieCoverImagePage.col().find({MovieCoverImagePage.image_content.name: {"$exists": True}}).count() \
    #        == n_movie

    session.close()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
