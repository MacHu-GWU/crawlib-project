# -*- coding: utf-8 -*-

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mate import ExtendedBase

from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session

Base = declarative_base()


class DummyForTest(Base, ExtendedBase):
    __tablename__ = "dummy_for_test"

    id = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String)


def test_db_connect():
    Base.metadata.create_all(engine)
    DummyForTest.smart_insert(engine, DummyForTest(id=1, value="Hello!"))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
