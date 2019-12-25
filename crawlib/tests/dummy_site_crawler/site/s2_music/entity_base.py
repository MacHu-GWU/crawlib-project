# -*- coding: utf-8 -*-

import requests
from crawlib2.entity.mongodb.entity import MongodbEntitySingleStatus


class MusicWebsiteEntity(MongodbEntitySingleStatus):
    meta = {
        "abstract": True,
    }

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)
