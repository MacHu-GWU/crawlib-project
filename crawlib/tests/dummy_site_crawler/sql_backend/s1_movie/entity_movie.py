# -*- coding: utf-8 -*-

import requests
import sqlalchemy as sa

from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig
from crawlib.entity.sql import SqlEntity, SqlEntitySingleStatus
from .url_builder import url_builder


class MoviePageBase(SqlEntity):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    status_movie_info = sa.Column(sa.Integer)
    edit_at_movie_info = sa.Column(sa.DateTime)

    image_content = sa.Column(sa.String)
    status_cover_image = sa.Column(sa.Integer)
    edit_at_cover_image = sa.Column(sa.DateTime)

    @property
    def movie_id(self):
        return self.id

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class MovieCoverImagePage(MoviePageBase):
    __tablename__ = "site_movie_movie"
    __table_args__ = {"extend_existing": True}

    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_cover_image"
    CONF_EDIT_AT_KEY = "edit_at_cover_image"
    CONF_UPDATE_FIELDS = (
        "image_content",
    )

    def build_url(self):
        return url_builder.url_movie_detail(self.id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        entity = self.__class__(image_content=html)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            data={},
            status=status,
        )
        return pres


MovieCoverImagePage.validate_implementation()


class MoviePage(MoviePageBase):
    __tablename__ = "site_movie_movie"
    __table_args__ = {"extend_existing": True}

    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_movie_info"
    CONF_EDIT_AT_KEY = "edit_at_movie_info"
    CONF_UPDATE_FIELDS = (
        "title",
    )

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MovieCoverImagePage, Relationship.Option.one, recursive=True)
    ])

    def build_url(self):
        return url_builder.url_movie_detail(self.id)

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


class ListPage(SqlEntitySingleStatus):
    __tablename__ = "site_movie_listpage"

    CONF_UPDATE_INTERVAL = 1
    CONF_UPDATE_FIELDS = (
        "n_movie",
    )

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MoviePage, Relationship.Option.many, "n_movie", recursive=True)
    ])

    id = sa.Column(sa.Integer, primary_key=True)
    n_movie = sa.Column(sa.Integer)

    @property
    def page_num(self):
        return self.id

    def build_url(self):
        return url_builder.url_nth_listpage(self.page_num)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        div_listpage = soup.find("div", id="listpage")
        a_tag_list = div_listpage.find_all("a")

        entity = ListPage()

        children = list()
        for a in a_tag_list:
            href = a["href"]
            movie_id = int(href.split("/")[-1])
            movie = MoviePage(id=movie_id)
            children.append(movie)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


ListPage.validate_implementation()


class HomePage(SqlEntitySingleStatus):
    __tablename__ = "site_movie_homepage"

    CONF_UPDATE_INTERVAL = 1
    CONF_UPDATE_FIELDS = (
        "description",
        "max_page_num",
        "n_listpage",
    )
    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(ListPage, Relationship.Option.many, "n_listpage", recursive=True)
    ])

    id = sa.Column(sa.Integer, primary_key=True)
    description = sa.Column(sa.String)
    max_page_num = sa.Column(sa.Integer)
    n_listpage = sa.Column(sa.Integer)

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
            listpage = ListPage(id=page_num)
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
