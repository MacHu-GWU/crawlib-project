#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawlib_doc.db import client, db, dbname
from mongoengine_mate import ExtendedDocument
from mongoengine import fields



class BaseUser(ExtendedDocument):
    _id = fields.IntField(primary_key=True)
    name = fields.StringField()
    dob = fields.StringField()

    _st_name= fields.IntField()
    _st_dob = fields.IntField()

    meta = {
        "abstract": True,
        "db_alias": dbname,
        "collection": "user",
    }


class User1(BaseUser):
    status_key = BaseUser._st_name.name

    # meta = {"db_alias": dbname, "collection": "user"}

class User2(BaseUser):
    status_key = BaseUser._st_dob.name

    # meta = {"db_alias": dbname, "collection": "user"}


User1.smart_insert(User1(_id=1, name="Alice", _st_name=1))
User2.smart_insert(User2(_id=2, dob="2000-01-01", _st_dob=2))

print(User1.objects().all())

