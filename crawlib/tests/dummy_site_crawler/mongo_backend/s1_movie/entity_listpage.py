# -*- coding: utf-8 -*-

from mongoengine import fields
from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig
from crawlib.tests.dummy_site_crawler.mongo_backend.config_init import config

from .entity_base import MovieWebsiteEntity
from .entity_movie import MoviePage
from ...movie_url_builder import url_builder


class ListPage(MovieWebsiteEntity):
    CONF_UPDATE_INTERVAL = 1
    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MoviePage, Relationship.Option.many, "n_movie", recursive=True)
    ])

    _id = fields.IntField(primary_key=True)
    n_movie = fields.IntField()

    meta = dict(
        collection="site_movie_listpage",
        db_alias=config.DB_DATABASE.get_value(),
    )

    @property
    def page_num(self):
        return self._id

    def build_url(self):
        return url_builder.url_nth_listpage(self.page_num)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        div_listpage = soup.find("div", id="listpage")
        a_tag_list = div_listpage.find_all("a")

        entity_data = dict()

        children = list()
        for a in a_tag_list:
            href = a["href"]
            movie_id = int(href.split("/")[-1])
            movie = MoviePage(_id=movie_id)
            children.append(movie)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


ListPage.validate_implementation()
