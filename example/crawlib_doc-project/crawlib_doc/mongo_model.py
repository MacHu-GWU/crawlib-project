#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import fields
from crawlib import mongodb, Status
from datetime import datetime

try:
    from .url_builder import url_builder
    from .mongo_db import client, db, dbname
except:
    from crawlib_doc.url_builder import url_builder
    from crawlib_doc.mongo_db import client, db, dbname


class Thing(mongodb.ExtendedDocument):
    _id = fields.StringField(primary_key=True)
    name = fields.StringField()
    n_child = fields.IntField()
    _status = fields.IntField(default=Status.S0_ToDo.id)
    _edit_at = fields.DateTimeField(default=datetime(1970, 1, 1))

    meta = {
        "abstract": True,
        "db_alias": dbname,
    }

    _settings_STATUS_KEY_required = "_status"
    _settings_EDIT_AT_KEY_required = "_edit_at"


class State(Thing):
    def build_url(self):
        return url_builder.build_city_listpage(self._id)


State.validate_implementation()


class City(Thing):
    def build_url(self):
        return url_builder.build_zipcode_listpage(self._id)


City.validate_implementation()


class Zipcode(Thing):
    pass


Zipcode.validate_implementation()

c_state = db[State.col().name]
c_city = db[City.col().name]
c_zipcode = db[Zipcode.col().name]
