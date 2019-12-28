# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
import sqlalchemy as sa

from crawlib import Status
from crawlib.entity.sql.entity import Base, SqlEntitySingleStatus
from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session


class TestSqlEntity(object):
    def test_get_finished_unfinished(self):
        class DummyEntityForTest(SqlEntitySingleStatus):
            __tablename__ = "dummy_entity_for_test"

            id = sa.Column(sa.Integer, primary_key=True)
            value = sa.Column(sa.String, nullable=True)

            CONF_UPDATE_INTERVAL = 1
            CONF_STATUS_KEY = "status"
            CONF_EDIT_AT_KEY = "edit_at"
            CONF_UPDATE_FIELDS = (
                "value",
            )

        Base.metadata.create_all(engine)

        session = Session()

        session.query(DummyEntityForTest).delete()
        DummyEntityForTest.smart_insert(
            session,
            [
                DummyEntityForTest(id=1, value="Alice", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=2, value="Bob", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=3, value="Cathy", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=4, value="David", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=5, value="Edward", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=6, value="Frank", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(id=7, value="George", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
            ]
        )
        assert DummyEntityForTest.count_unfinished(session) == 3
        assert DummyEntityForTest.count_unfinished(session, filters=(DummyEntityForTest.id <= 3,)) == 1
        assert DummyEntityForTest.count_unfinished(session, filters=(DummyEntityForTest.id > 3,)) == 2
        for row in DummyEntityForTest.get_unfinished(session,
                                                     only_fields=[DummyEntityForTest.id, DummyEntityForTest.value]):
            assert len(row) == 2

        assert DummyEntityForTest.count_finished(session) == 4
        assert DummyEntityForTest.count_finished(session, filters=(DummyEntityForTest.id <= 3,)) == 2
        assert DummyEntityForTest.count_finished(session, filters=(DummyEntityForTest.id > 3,)) == 2
        for row in DummyEntityForTest.get_finished(session,
                                                   only_fields=[DummyEntityForTest.id, DummyEntityForTest.value]):
            assert len(row) == 2

        session.commit()
        session.close()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
