# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site.config import PORT
from crawlib.middleware.url_builder import BaseUrlBuilder


class UrlBuilder(BaseUrlBuilder):
    domain = "http://127.0.0.1:{}".format(PORT)

    def url_random_music(self):
        return self.join_all("music", "random")

    def url_artist(self, artist_id):
        return self.join_all("music", "artist", str(artist_id))

    def url_genre(self, genre_id):
        return self.join_all("music", "genre", str(genre_id))

    def url_music_detail(self, music_id):
        return self.join_all("music", str(music_id))


url_builder = UrlBuilder()
