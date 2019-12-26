# -*- coding: utf-8 -*-

import requests
from crawlib.entity.mongodb import MongodbEntitySingleStatus


class MovieWebsiteEntity(MongodbEntitySingleStatus):
    meta = {
        "abstract": True,
    }

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)
