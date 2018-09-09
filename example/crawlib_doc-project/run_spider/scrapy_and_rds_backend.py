#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use scrapy framework.
"""

from scrapy.crawler import CrawlerProcess
from sqlalchemy.orm import sessionmaker
from crawlib_doc import spiders
from crawlib_doc.rds_db import engine
from crawlib_doc.rds_model import State, City, Zipcode

if __name__ == "__main__":
    spider = spiders.StateListpage
    # spider = spiders.CityListpage
    # spider = spiders.ZipcodeListpage

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


    process.crawl(spider)
    process.start()

    def print_result():
        ses = sessionmaker(bind=engine)()
        for state in ses.query(State):
            print(state)
        for city in ses.query(City):
            print(city)
        for zipcode in ses.query(Zipcode):
            print(zipcode)
        ses.close()


    print_result()
