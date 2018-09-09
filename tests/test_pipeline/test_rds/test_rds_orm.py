#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import rolex
import random
from datetime import datetime
from crawlib import Status
from crawlib.pipeline.rds.orm import ExtendedBase
from sqlalchemy_mate import engine_creator

from sqlalchemy import Column
from sqlalchemy import Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


@pytest.fixture
def engine():
    return engine_creator.create_sqlite()


class TestRdsOrm(object):
    def test_validate_implementation(self):
        Base = declarative_base()

        # _settings_STATUS_KEY_required not defined
        class A(Base, ExtendedBase):
            __tablename__ = "a"

            _id = Column(Integer, primary_key=True)

        with pytest.raises(NotImplementedError):
            A.validate_implementation()

        # status column not declared
        class B(Base, ExtendedBase):
            __tablename__ = "b"

            _id = Column(Integer, primary_key=True)

            _settings_STATUS_KEY_required = "status"
            _settings_EDIT_AT_KEY_required = "edit_at"

        with pytest.raises(NotImplementedError):
            B.validate_implementation()

        # key name and column name not match
        class C(Base, ExtendedBase):
            __tablename__ = "c"

            _id = Column(Integer, primary_key=True)
            _status = Column(Integer)
            _edit_at = Column(DateTime)

            _settings_STATUS_KEY_required = "status"
            _settings_EDIT_AT_KEY_required = "edit_at"

        with pytest.raises(NotImplementedError):
            C.validate_implementation()

        # correct
        class D(Base, ExtendedBase):
            __tablename__ = "d"

            _id = Column(Integer, primary_key=True)
            status = Column(Integer)
            edit_at = Column(DateTime)

            _settings_STATUS_KEY_required = "status"
            _settings_EDIT_AT_KEY_required = "edit_at"

        D.validate_implementation()


class TestQueryBuilder(object):
    def test_finished_unfinished(self, engine):
        Base = declarative_base()

        status_key, edit_at_key = "status", "edit_at"

        class User(Base, ExtendedBase):
            __tablename__ = "user"

            _id = Column(Integer, primary_key=True)
            status = Column(Integer)
            edit_at = Column(DateTime)

            _settings_STATUS_KEY_required = status_key
            _settings_EDIT_AT_KEY_required = edit_at_key
            _settings_UPDATE_INTERVAL_required = 24 * 3600

        Base.metadata.create_all(engine)

        engine.execute(
            User.__table__.insert(),
            [
                {
                    status_key: random.randint(Status.S0_ToDo.id, Status.S99_Finalized.id),
                    edit_at_key: rolex.add_hours(datetime.now(), random.randint(-48, 0))
                } for _ in range(100)
            ],
        )

        finished_count = len(User.get_all_finished(engine))
        for user in User.get_all_finished(engine):
            assert user.status >= 50
            assert (datetime.now() - user.edit_at).total_seconds() <= 24 * 3600

        unfinished_count = len(User.get_all_unfinished(engine))
        for user in User.get_all_unfinished(engine):
            assert (user.status < 50) or (
                    (datetime.now() - user.edit_at).total_seconds() > 24 * 3600)

        assert (finished_count + unfinished_count) == 100


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
