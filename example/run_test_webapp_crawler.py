# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site_crawler.db import db
from crawlib.tests.dummy_site_crawler.site.s1_movie import (
    HomePage, ListPage, MoviePage, MovieCoverImagePage,
)

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
# ListPage.start_all()


# MoviePage.start_all()
# print(MovieCoverImagePage.get_unfinished())

# import datetime
# from crawlib.entity.mongodb import query_builder
#
# query_filters = query_builder.unfinished(
#     finished_status=MovieCoverImagePage.CONF_FINISHED_STATUS,
#     update_interval=MovieCoverImagePage.CONF_UPDATE_INTERVAL,
#     status_key=MovieCoverImagePage.CONF_STATUS_KEY,
#     edit_at_key=MovieCoverImagePage.CONF_EDIT_AT_KEY,
# )
# print(MovieCoverImagePage, query_filters, MovieCoverImagePage.by_filter(query_filters).count())
