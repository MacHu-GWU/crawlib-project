#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import fields
from crawlib import mongodb, Status
from datetime import datetime
from crawlib.pipeline.mongodb.scheduler import QueryBuilder
try:
    from .url_builder import url_builder
    from .db import client, db, dbname
except:
    from crawlib_doc.url_builder import url_builder
    from crawlib_doc.db import client, db, dbname


class Thing(mongodb.ExtendedDocument):
    _id = fields.StringField(primary_key=True)
    name = fields.StringField()
    _status = fields.IntField(default=Status.S0_ToDo.id)
    _edit_at = fields.DateTimeField(default=datetime(1970, 1, 1))

    meta = {
        "abstract": True,
        "db_alias": dbname,
    }

    status_key = "_status"
    edit_at_key = "_edit_at"

    @classmethod
    def get_all_unfinished(cls):
        filters = QueryBuilder.unfinished(
            finished_status=Status.S50_Finished.id,
            update_interval=7*24*3600,
            status_key=cls.status_key,
            edit_at_key=cls.edit_at_key,
        )
        return cls.by_filter(filters)


class State(Thing):
    n_city = fields.IntField()

    n_children_key = "n_city"

    def build_url(self):
        return url_builder.build_city_listpage(self._id)


class City(Thing):
    n_zipcode = fields.IntField()

    n_children_key = "n_zipcode"

    def build_url(self):
        return url_builder.build_zipcode_listpage(self._id)


class Zipcode(Thing):
    meta = {"db_alias": dbname}


c_state = db[State.col().name]
c_city = db[City.col().name]
c_zipcode = db[Zipcode.col().name]
