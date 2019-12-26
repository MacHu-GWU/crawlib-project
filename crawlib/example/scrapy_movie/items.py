# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import mongoengine as me
import scrapy
import pymongo
from mongoengine_mate import ExtendedDocument

from .config import Config
from .db import client, db

c_movie_listpage = db["movie_listpage"] # type: pymongo.collection.Collection
c_movie = db["movie"] # type: pymongo.collection.Collection


class MovieListPage(ExtendedDocument):
    _id = me.fields.IntField(primary_key=True)
    status = me.fields.IntField()
    edit_at = me.fields.DateTimeField()

    meta = dict(
        collection="site_movie_listpage",
        db_alias=Config.MongoDB.database,
    )


class ScrapyMovieListpageItem(scrapy.Item):
    _id = scrapy.Field()
    status = scrapy.Field()
    edit_at = scrapy.Field()

    def build_url(self):
        return "{}/movie/listpage/{}".format(Config.Url.domain, self._id)

    def process(self):
        c_movie_listpage.update_one(
            filter={"_id": self["_id"]},
            update={"$set": dict(self)},
            upsert=True,
        )

class ScrapyMovieItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    edit_at = scrapy.Field()

    def process(self):
        c_movie.update_one(
            filter={"_id": self["_id"]},
            update={"$set": dict(self)},
            upsert=True,
        )
