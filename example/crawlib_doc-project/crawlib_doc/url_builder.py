#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .constant import DOMAIN
from crawlib import BaseUrlBuilder


class UrlBuilder(BaseUrlBuilder):
    def build_state_listpage(self):
        return self.join_all("_static", "state-list.html")

    def build_city_listpage(self, state_key):
        return self.join_all("_static", state_key + ".html")

    def build_zipcode_listpage(self, city_key):
        return self.join_all("_static", city_key + ".html")


url_builder = UrlBuilder(domain=DOMAIN)
