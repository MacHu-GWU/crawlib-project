# -*- coding: utf-8 -*-

"""
Verify that mongoengine ORM framework allow mixin class declaration.

Verify that mongoengine ORM framework use None in app data if the Attribute
are not given.
"""

import mongoengine as me
import pytest
from mongoengine_mate import ExtendedDocument


class UserAttributeMixin(object):
    _id = me.fields.IntField(primary_key=True)
    name = me.fields.StringField()
    status = me.fields.IntField(default=0)


class User(ExtendedDocument, UserAttributeMixin):
    pass


class Test(object):
    def test(self):
        user = User()
        assert user._id is None

        user = User(id=1)
        assert user.name is None
        assert user.status == 0
        assert user.to_dict() == {"_id": 1, "name": None, "status": 0}

        user = User(id=1, name="Alice")
        assert user.status == 0
        assert user.to_dict() == {"_id": 1, "name": "Alice", "status": 0}


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
