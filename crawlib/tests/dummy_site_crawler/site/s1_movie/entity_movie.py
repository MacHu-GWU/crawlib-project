# -*- coding: utf-8 -*-

import requests
from mongoengine import fields

from crawlib import Status, ParseResult, resolve_arg, time_util, Relationship, RelationshipConfig
from crawlib.entity.mongodb import MongodbEntity
from .url_builder import url_builder
from ...config import Config


class MoviePageBase(MongodbEntity):
    _id = fields.IntField(primary_key=True)
    title = fields.StringField()
    status_movie_info = fields.IntField(default=Status.S0_ToDo.id)
    edit_at_movie_info = fields.DateTimeField(default=lambda: time_util.epoch)

    image_content = fields.StringField()
    status_cover_image = fields.IntField(default=Status.S0_ToDo.id)
    edit_at_cover_image = fields.DateTimeField(default=lambda: time_util.epoch)

    meta = {
        "abstract": True,
    }

    @property
    def movie_id(self):
        return self._id

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class MovieCoverImagePage(MoviePageBase):
    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_cover_image"
    CONF_EDIT_AT_KEY = "edit_at_cover_image"
    CONF_UPDATE_FIELDS = (
        "image_content",
    )

    meta = dict(
        collection="site_movie_movie",
        db_alias=Config.MongoDB.database,
    )

    def build_url(self):
        return url_builder.url_movie_detail(self._id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        entity = MovieCoverImagePage(image_content=html)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            data={},
            status=status,
        )
        return pres


MovieCoverImagePage.validate_implementation()


class MoviePage(MoviePageBase):
    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_movie_info"
    CONF_EDIT_AT_KEY = "edit_at_movie_info"
    CONF_UPDATE_FIELDS = (
        "title",
    )

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MovieCoverImagePage, Relationship.Option.one, recursive=True)
    ])

    meta = dict(
        collection="site_movie_movie",
        db_alias=Config.MongoDB.database,
    )

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
