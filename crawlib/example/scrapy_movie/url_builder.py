# -*- coding: utf-8 -*-

from .config import Config

class UrlBuilder(object):
    def listpage_url(self, listpage_id):
        return "{}/listpage/{}".format(Config.Url.domain, listpage_id)

url_builder = UrlBuilder()
