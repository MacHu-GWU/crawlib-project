# -*- coding: utf-8 -*-

"""
Verify that sqlalchemy ORM framework allow mixin class declaration.

Verify that sqlalchemy ORM framework use None in app data if the Attribute
are not given.
"""

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mate import ExtendedBase

Base = declarative_base()


class UserAttributeMixin(object):
    name = sa.Column(sa.String)
    status = sa.Column(sa.Integer, default=0)


class User(Base, UserAttributeMixin, ExtendedBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)


class Test(object):
    def test(self):
        user = User()
        assert user.id is None

        user = User(id=1)
        assert user.name is None
        assert user.status is None
        assert user.to_dict() == {"id": 1, "name": None, "status": None}

        user = User(id=1, name="Alice")
        assert user.status is None
        assert user.to_dict() == {"id": 1, "name": "Alice", "status": None}


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
