# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site.config import PORT
from crawlib.middleware.url_builder import BaseUrlBuilder


class UrlBuilder(BaseUrlBuilder):
    domain = "http://127.0.0.1:{}".format(PORT)

    def url_first_listpage(self):
        return self.join_all("movie", "listpage", str(1))

    def url_nth_listpage(self, nth):
        return self.join_all("movie", "listpage", str(nth))

    def url_movie_detail(self, movie_id):
        return self.join_all("movie", str(movie_id))

url_builder = UrlBuilder()
