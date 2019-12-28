# -*- coding: utf-8 -*-

from mongoengine import fields
from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig
from crawlib.tests.dummy_site_crawler.mongo_backend.config_init import config

from .entity_base import MovieWebsiteEntity
from .entity_listpage import ListPage
from ...movie_url_builder import url_builder


class HomePage(MovieWebsiteEntity):
    CONF_UPDATE_INTERVAL = 1
    CONF_UPDATE_FIELDS = (
        "description",
        "max_page_num",
        "n_listpage",
    )
    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(ListPage, Relationship.Option.many, "n_listpage", recursive=True)
    ])

    _id = fields.IntField(primary_key=True)
    description = fields.StringField()
    max_page_num = fields.IntField()
    n_listpage = fields.IntField()

    meta = dict(
        collection="site_movie_homepage",
        db_alias=config.DB_DATABASE.get_value(),
    )

    def build_url(self, **kwargs):
        return url_builder.url_first_listpage()

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        div_pagination = soup.find("div", id="pagination")
        a_tag_list = div_pagination.find_all("a")
        href = a_tag_list[-1]["href"]
        max_page_num = int(href.split("/")[-1])
        entity = HomePage(max_page_num=max_page_num)

        children = list()
        for page_num in range(1, 1 + max_page_num):
            listpage = ListPage(_id=page_num)
            children.append(listpage)

        status = Status.S50_Finished.id
        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


HomePage.validate_implementation()
