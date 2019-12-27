# -*- coding: utf-8 -*-

import pytest
from crawlib.tests.dummy_site_crawler.db import client, db
from crawlib.tests.dummy_site_crawler.site.s1_movie import (
    HomePage,
    ListPage,
    MoviePage,
)
from crawlib.tests.dummy_site.movie.view import n_movie, max_page_id


def test():
    HomePage(_id=1).save()
    assert HomePage.col().find().count() == 1
    assert ListPage.col().find().count() == 0
    assert MoviePage.col().find().count() == 0

    HomePage.start_all(detailed_log=True)
    
    assert HomePage.col().find().count() == 1
    assert ListPage.col().find().count() == max_page_id
    assert MoviePage.col().find().count() == n_movie

    assert HomePage.col().find_one()[HomePage.n_listpage.name] == 10
    for doc in ListPage.col().find():
        assert doc[ListPage.n_movie.name] in [10, 8]

    for doc in MoviePage.col().find():
        assert doc[MoviePage.title.name] == "Movie %s Title" % doc[MoviePage._id.name]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
