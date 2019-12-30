# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from mongoengine import fields

from crawlib import resolve_arg
from crawlib.entity.base import RelationshipConfig, Relationship, ParseResult
from crawlib.status import Status
from crawlib.tests.dummy_site_crawler.mongo_backend.config_init import config
from .entity_base import MusicWebsiteEntity
from ...music_url_builder import url_builder


class MusicPage(MusicWebsiteEntity):
    CONF_UPDATE_INTERVAL = 24 * 3600

    _id = fields.IntField(primary_key=True)
    title = fields.StringField()

    artists = fields.ListField(fields.IntField())
    n_artist = fields.IntField()

    genres = fields.ListField(fields.IntField())
    n_genre = fields.IntField()

    meta = dict(
        collection="site_music_music",
        db_alias=config.DB_DATABASE.get_value(),
    )

    @property
    def music_id(self):
        return self._id

    def build_url(self):
        return url_builder.url_music_detail(self._id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        div_detail = soup.find("div", id="detail")
        title = div_detail.find("div", class_="title").find("span").text
        artists = [
            int(a["href"].split("/")[-1])
            for a in div_detail.find("div", class_="artists").find_all("a")
        ]
        genres = [
            int(a["href"].split("/")[-1])
            for a in div_detail.find("div", class_="genres").find_all("a")
        ]

        entity_data = dict(title=title, artists=artists, genres=genres)
        children = list()
        for artist_id in artists:
            children.append(ArtistPage(_id=artist_id))
        for genre_id in genres:
            children.append(GenrePage(_id=genre_id))

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


class ArtistPage(MusicWebsiteEntity):
    CONF_UPDATE_INTERVAL = 3600
    CONF_UPDATE_FIELDS = ("musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music", recursive=False)
    ])

    _id = fields.IntField(primary_key=True)
    musics = fields.ListField(fields.IntField())
    n_music = fields.IntField()

    meta = dict(
        collection="site_music_artist",
        db_alias=config.DB_DATABASE.get_value(),
    )

    @property
    def artist_id(self):
        return self._id

    def build_url(self):
        return url_builder.url_artist(self._id)

    def parse_response(self, url, request, response, html=None, **kwargs):
        if html is None:
            html = response.text

        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", id="detail")
        musics = [
            int(a["href"].split("/")[-1])
            for a in div.find_all("a")
        ]
        entity_data = dict(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(_id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


class GenrePage(MusicWebsiteEntity):
    CONF_UPDATE_INTERVAL = 3600
    CONF_UPDATE_FIELDS = ("musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music", recursive=False)
    ])

    _id = fields.IntField(primary_key=True)
    musics = fields.ListField(fields.IntField())
    n_music = fields.IntField()

    meta = dict(
        collection="site_music_genre",
        db_alias=config.DB_DATABASE.get_value(),
    )

    @property
    def genre_id(self):
        return self._id

    def build_url(self):
        return url_builder.url_genre(self._id)

    def parse_response(self, url, request, response, html=None, **kwargs):
        if html is None:
            html = response.text

        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", id="detail")
        musics = [
            int(a["href"].split("/")[-1])
            for a in div.find_all("a")
        ]
        entity_data = dict(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(_id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


class RandomMusicPage(MusicWebsiteEntity):
    CONF_UPDATE_INTERVAL = 1
    CONF_UPDATE_FIELDS = ("musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music")
    ])

    _id = fields.IntField(primary_key=True)
    musics = fields.ListField(fields.IntField())
    n_music = fields.IntField()

    meta = dict(
        collection="site_music_random_music",
        db_alias=config.DB_DATABASE.get_value(),
    )

    def build_url(self, **kwargs):
        return url_builder.url_random_music()

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        musics = [
            int(a["href"].split("/")[-1])
            for a in soup.find_all("a")
        ]
        entity_data = dict(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(_id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity_data=entity_data,
            children=children,
            additional_data={},
            status=status,
        )
        return pres


MusicPage.CONF_RELATIONSHIP = RelationshipConfig([
    Relationship(ArtistPage, Relationship.Option.many, "n_artist"),
    Relationship(GenrePage, Relationship.Option.many, "n_genre"),
])

MusicPage.validate_implementation()
ArtistPage.validate_implementation()
GenrePage.validate_implementation()
RandomMusicPage.validate_implementation()
