# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from crawlib import mongodb
from .model import State, City, Zipcode


StateItem = mongodb


class CrawlibDocItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
