#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from crawlib_doc import spiders
from crawlib_doc.mongo_db import db
from crawlib_doc.mongo_model import (
    State as StateMongp,
    City as CityMongo,
    Zipcode as ZipcodeMongo,
)
from crawlib_doc.rds_db import engine
from crawlib_doc.mongo_model import (
    State as StateRds,
    City as CityRds,
    Zipcode as ZipcodeRds,
)
import mongomock_mate
from pathlib_mate import Path


if __name__ == "__main__":
    spider = spiders.StateListpage
    # spider = spiders.CityListpage
    # spider = spiders.ZipcodeListpage

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(spider)
    process.start()
