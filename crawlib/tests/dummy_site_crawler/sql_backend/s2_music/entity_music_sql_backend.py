# -*- coding: utf-8 -*-

import typing

import requests
import sqlalchemy as sa

from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig
from crawlib.entity.sql import Base, SqlEntitySingleStatus
from ...music_url_builder import url_builder


class MusicPageBase(SqlEntitySingleStatus):
    __abstract__ = True

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class MusicPage(MusicPageBase):
    __tablename__ = "site_music_music"

    CONF_UPDATE_INTERVAL = 24 * 3600
    CONF_UPDATE_FIELDS = (
        "id", "title", "artists", "n_artist", "genres", "n_genre",
    )

    id = sa.Column(sa.Integer, primary_key=True)  # type: int
    title = sa.Column(sa.String)  # type: title

    artists = sa.Column(sa.PickleType)  # type: typing.List[int]
    n_artist = sa.Column(sa.Integer)  # type: int

    genres = sa.Column(sa.PickleType)  # type: typing.List[int]
    n_genre = sa.Column(sa.Integer)  # type: int

    @property
    def music_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_music_detail(self.music_id)

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

        entity = MusicPage(title=title, artists=artists, genres=genres)
        children = list()
        for artist_id in artists:
            children.append(ArtistPage(id=artist_id))
        for genre_id in genres:
            children.append(GenrePage(id=genre_id))

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


class ArtistPage(MusicPageBase):
    __tablename__ = "site_music_artist"

    CONF_UPDATE_INTERVAL = 3600
    CONF_UPDATE_FIELDS = ("id", "musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music", recursive=False)
    ])

    id = sa.Column(sa.Integer, primary_key=True)  # type: int
    musics = sa.Column(sa.PickleType)  # type: typing.List[int]
    n_music = sa.Column(sa.Integer)  # type: int

    @property
    def artist_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_artist(self.artist_id)

    @resolve_arg()
    def parse_response(self, url, request, response, html=None, soup=None, **kwargs):
        div = soup.find("div", id="detail")
        musics = [
            int(a["href"].split("/")[-1])
            for a in div.find_all("a")
        ]
        entity = ArtistPage(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


class GenrePage(MusicPageBase):
    __tablename__ = "site_music_genre"
    CONF_UPDATE_INTERVAL = 3600
    CONF_UPDATE_FIELDS = ("id", "musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music", recursive=False)
    ])

    id = sa.Column(sa.Integer, primary_key=True)  # type: int
    musics = sa.Column(sa.PickleType)  # type: typing.List[int]
    n_music = sa.Column(sa.Integer)  # type: int

    @property
    def genre_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_genre(self.genre_id)

    @resolve_arg()
    def parse_response(self, url, request, response, html=None, soup=None, **kwargs):
        div = soup.find("div", id="detail")
        musics = [
            int(a["href"].split("/")[-1])
            for a in div.find_all("a")
        ]
        entity = GenrePage(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


class RandomMusicPage(MusicPageBase):
    __tablename__ = "site_music_random_music"
    CONF_UPDATE_INTERVAL = 1
    CONF_UPDATE_FIELDS = ("id", "musics", "n_music")

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music")
    ])

    id = sa.Column(sa.Integer, primary_key=True)  # type: int
    musics = sa.Column(sa.PickleType)  # type: typing.List[int]
    n_music = sa.Column(sa.Integer)  # type: int

    def build_url(self, **kwargs):
        return url_builder.url_random_music()

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        musics = [
            int(a["href"].split("/")[-1])
            for a in soup.find_all("a")
        ]
        entity = RandomMusicPage(musics=musics)

        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
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
