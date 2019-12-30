# -*- coding: utf-8 -*-

import requests
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig, epoch
from crawlib.entity.sql import SqlEntity, SqlEntitySingleStatus
from ...movie_url_builder import url_builder


# due to sqlalchemy design, single Base can not has two subclass having the same
# table name
Base1 = declarative_base()
Base2 = declarative_base()


class MoviePageBase(SqlEntity):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    status_movie_info = sa.Column(sa.Integer, default=Status.S0_ToDo.id)
    edit_at_movie_info = sa.Column(sa.DateTime, default=epoch)

    image_content = sa.Column(sa.String)
    status_cover_image = sa.Column(sa.Integer, default=Status.S0_ToDo.id)
    edit_at_cover_image = sa.Column(sa.DateTime, default=epoch)

    @property
    def movie_id(self):
        return self.id

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class MovieCoverImagePage(Base1, MoviePageBase):
    __tablename__ = "site_movie_movie"

    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_cover_image"
    CONF_EDIT_AT_KEY = "edit_at_cover_image"

    def build_url(self):
        return url_builder.url_movie_detail(self.id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        status = Status.S50_Finished.id
        entity_data = dict(image_content=html)
        pres = ParseResult(
            entity_data=entity_data,
            additional_data={},
            status=status,
        )
        return pres


MovieCoverImagePage.validate_implementation()


class MoviePage(Base2, MoviePageBase):
    __tablename__ = "site_movie_movie"

    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_STATUS_KEY = "status_movie_info"
    CONF_EDIT_AT_KEY = "edit_at_movie_info"

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MovieCoverImagePage, Relationship.Option.one, recursive=True)
    ])

    def build_url(self):
        return url_builder.url_movie_detail(self.id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        span_title = soup.find("span", class_="title")
        title = span_title.text
        entity_data = dict(title=title)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            additional_data={},
            status=status,
        )
        return pres


MoviePage.validate_implementation()


class SingleStatusEntityBase(Base1, SqlEntitySingleStatus):
    __abstract__ = True

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class ListPage(SingleStatusEntityBase):
    __tablename__ = "site_movie_listpage"

    CONF_UPDATE_INTERVAL = 1

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

        entity_data = {}

        children = list()
        for a in a_tag_list:
            href = a["href"]
            movie_id = int(href.split("/")[-1])
            movie = MoviePage(id=movie_id)
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


class HomePage(SingleStatusEntityBase):
    __tablename__ = "site_movie_homepage"

    CONF_UPDATE_INTERVAL = 1
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
        entity_data = dict(max_page_num=max_page_num)

        children = list()
        for page_num in range(1, 1 + max_page_num):
            listpage = ListPage(id=page_num)
            children.append(listpage)

        status = Status.S50_Finished.id
        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


HomePage.validate_implementation()
