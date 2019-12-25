# -*- coding: utf-8 -*-

from mongoengine import fields
from crawlib2 import Status
from crawlib2 import Relationship, RelationshipConfig, ParseResult
from crawlib2 import resolve_arg

from .url_builder import url_builder
from .entity_base import MusicWebsiteEntity
from .entity_music import MusicPage
from ...config import Config


class RandomMusicPage(MusicWebsiteEntity):
    CONF_UPDATE_INTERVAL = 1

    CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(MusicPage, Relationship.Option.many, "n_music")
    ])

    _id = fields.IntField(primary_key=True)
    musics = fields.ListField(fields.IntField())
    n_music = fields.IntField()

    meta = dict(
        collection="site_music_random_music",
        db_alias=Config.MongoDB.database,
    )

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
            music = MusicPage(_id=music_id)
            children.append(music)

        status = Status.S50_Finished.id

        pres = ParseResult(
            entity=entity,
            children=children,
            data={},
            status=status,
        )
        return pres


RandomMusicPage.validate_implementation()
