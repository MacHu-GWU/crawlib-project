# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from mongoengine import fields
from crawlib2 import Status, ParseResult, resolve_arg
from .url_builder import url_builder
from .entity_base import MovieWebsiteEntity
from ...config import Config


class MoviePage(MovieWebsiteEntity):
    CONF_UPDATE_INTERVAL = 24 * 3600

    _id = fields.IntField(primary_key=True)
    title = fields.StringField()

    meta = dict(
        collection="site_movie_movie",
        db_alias=Config.MongoDB.database,
    )

    @property
    def movie_id(self):
        return self._id

    def build_url(self):
        return url_builder.url_movie_detail(self._id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        span_title = soup.find("span", class_="title")
        title = span_title.text
        entity = MoviePage(title=title)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            data={},
            status=status,
        )
        return pres


MoviePage.validate_implementation()
