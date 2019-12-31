# -*- coding: utf-8 -*-

import pytest

from crawlib.tests.dummy_site.movie.view import (
    n_movie, max_page_id, n_movie_each_page,
)
from crawlib.tests.dummy_site_crawler.mongo_backend.db import db
from crawlib.tests.dummy_site_crawler.mongo_backend.s1_movie import (
    HomePage,
    ListPage,
    MoviePage,
    MovieCoverImagePage,
)

_ = db


def setup_module():
    HomePage.col().delete_many({})
    ListPage.col().delete_many({})
    MoviePage.col().delete_many({})


@pytest.mark.order1
def test_start_recursive_crawler():
    assert HomePage.col().find().count() == 0
    assert ListPage.col().find().count() == 0
    assert MoviePage.col().find().count() == 0

    HomePage(_id=1).save()
    HomePage.start_recursive_crawler(detailed_log=True)

    assert HomePage.col().find().count() == 1
    assert ListPage.col().find().count() == max_page_id
    assert MoviePage.col().find().count() == n_movie

    assert HomePage.col().find_one()[HomePage.n_listpage.name] == max_page_id
    for doc in ListPage.col().find():
        assert doc[ListPage.n_movie.name] <= n_movie_each_page

    for doc in MoviePage.col().find():
        assert doc[MoviePage.title.name] == "Movie %s Title" % doc[MoviePage._id.name]

    assert MovieCoverImagePage.col().find({MovieCoverImagePage.image_content.name: {"$exists": True}}).count() \
           == n_movie


@pytest.mark.order2
def test_statistics():
    HomePage.print_statistics(seconds=3600)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
