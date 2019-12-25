# -*- coding: utf-8 -*-

from crawlib2.tests.dummy_site.music.app import PORT
from crawlib2.middleware.url_builder import BaseUrlBuilder


class UrlBuilder(BaseUrlBuilder):
    domain = "http://127.0.0.1:{}".format(PORT)

    def url_random_music(self):
        return self.join_all("random")

    def url_artist(self, artist_id):
        return self.join_all("artist", str(artist_id))

    def url_genre(self, genre_id):
        return self.join_all("genre", str(genre_id))

    def url_music_detail(self, music_id):
        return self.join_all("music", str(music_id))


url_builder = UrlBuilder()
