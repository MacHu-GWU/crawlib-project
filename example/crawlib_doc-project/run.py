#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from crawlib_doc import spiders
from crawlib_doc.db import db
from crawlib_doc.model import State, City, Zipcode
import mongomock_mate
from pathlib_mate import Path

if __name__ == "__main__":
    db_file = Path(__file__).change(new_basename="db.json").abspath

    # db.load_db(db_file)

    # spider = spiders.StateListpage
    # spider = spiders.CityListpage
    # spider = spiders.ZipcodeListpage

    print(list(State.col().find()))
    print(list(City.col().find()))
    print(list(Zipcode.col().find()))

    # print(list(db["state"].find()))
    # print(list(db["state"].find({'_status': {'$lt': 50}})))
    # print(list(State.col().find({'_status': {'$lt': 50}})))
    # print({'_status': {'$lt': 50}})
    # print(State.get_all_unfinished())
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    # process.crawl(spider)
    # process.start()

    # db.dump_db(db_file, pretty=True, overwrite=True)