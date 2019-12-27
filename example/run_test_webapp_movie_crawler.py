# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site_crawler.mongo_backend.s1_movie import (
    ListPage, MoviePage, )

# HomePage.smart_insert(HomePage(_id=1))
# HomePage.start_all()

indent = 0
unfinished_filters = {"_id": {"$lte": 2}}
n_unfinished = ListPage.count_unfinished(filters=unfinished_filters)
left_counter = n_unfinished
msg = "|%s| Working on Entity(%s), got %s url to crawl ..." % (indent, ListPage, n_unfinished)
ListPage.logger.info(msg, indent)
for listpage in list(ListPage.get_unfinished(filters=unfinished_filters)):
    left_counter -= 1
    listpage.start(left_counter=left_counter)
MoviePage.start_all()
