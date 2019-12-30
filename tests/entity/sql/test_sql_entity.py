# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from crawlib import Status
from crawlib.entity.sql.entity import SqlEntitySingleStatus
from crawlib.tests.dummy_site_crawler.sql_backend.db import engine, Session

Base = declarative_base()


class TestSqlEntity(object):
    def test_pre_process_only_fields_arg(self):
        class DummyEntityForOnlyFieldsArgTest(Base, SqlEntitySingleStatus):
            __tablename__ = "dummy_entity_for_only_fields_arg_test"

            id = sa.Column(sa.Integer, primary_key=True)
            value = sa.Column(sa.String, nullable=True)

        Base.metadata.create_all(engine)

        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(only_fields=None)
        assert is_partial_load is False
        assert len(only_column_names) == 0
        assert len(only_column_objects) == 0

        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(only_fields=("id",))
        assert is_partial_load is True
        assert only_column_names == ["id", ]
        assert only_column_objects == [DummyEntityForOnlyFieldsArgTest.id, ]

        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(
            only_fields=(DummyEntityForOnlyFieldsArgTest.id,))
        assert is_partial_load is True
        assert only_column_names == ["id", ]
        assert only_column_objects == [DummyEntityForOnlyFieldsArgTest.id, ]

        # edit `CONF_ONLY_FIELDS` config
        DummyEntityForOnlyFieldsArgTest.CONF_ONLY_FIELDS = ("id", "value")
        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(only_fields=None)
        assert is_partial_load is True
        assert only_column_names == ["id", "value"]
        assert only_column_objects == [DummyEntityForOnlyFieldsArgTest.id, DummyEntityForOnlyFieldsArgTest.value]

        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(only_fields=("id",))
        assert is_partial_load is True
        assert only_column_names == ["id", ]
        assert only_column_objects == [DummyEntityForOnlyFieldsArgTest.id, ]

        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = DummyEntityForOnlyFieldsArgTest._pre_process_only_fields_arg(
            only_fields=(DummyEntityForOnlyFieldsArgTest.id,))
        assert is_partial_load is True
        assert only_column_names == ["id", ]
        assert only_column_objects == [DummyEntityForOnlyFieldsArgTest.id, ]

    def test_all(self):
        class DummyEntityForTest(Base, SqlEntitySingleStatus):
            __tablename__ = "dummy_entity_for_test"

            id = sa.Column(sa.Integer, primary_key=True)
            value = sa.Column(sa.String, nullable=True)

            CONF_UPDATE_INTERVAL = 1
            CONF_STATUS_KEY = "status"
            CONF_EDIT_AT_KEY = "edit_at"
            CONF_UPDATE_FIELDS = (
                "value",
            )
            CONF_ONLY_FIELDS = (
                "id",
            )

        Base.metadata.create_all(engine)

        session = Session()

        # --- test SqlEntity.set_db_values() method ---
        session.query(DummyEntityForTest).delete()
        session.commit()
        DummyEntityForTest.smart_insert(engine, DummyEntityForTest(id=1, value="Alice"))

        DummyEntityForTest(id=1).set_db_values(engine=engine, data={"value": "Bob"})
        entity = DummyEntityForTest.by_id(1, session)
        assert entity.id == 1
        assert entity.value == "Bob"

        # --- test SqlEntity.get_unfinished(), SqlEntity.get_finished() methods ---
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

        for dummy_entity in DummyEntityForTest.get_unfinished(session):
            assert dummy_entity.status is None
            assert dummy_entity.edit_at is None

        for dummy_entity in DummyEntityForTest.get_unfinished(session, only_fields=["id", "status", "edit_at"]):
            assert dummy_entity.status is not None
            assert dummy_entity.edit_at is not None

        for dummy_entity in DummyEntityForTest.get_unfinished(
                session,
                only_fields=[
                    DummyEntityForTest.id,
                    DummyEntityForTest.status,
                    DummyEntityForTest.edit_at,
                ]
        ):
            assert dummy_entity.status is not None
            assert dummy_entity.edit_at is not None

        assert DummyEntityForTest.count_finished(session) == 4
        assert DummyEntityForTest.count_finished(session, filters=(DummyEntityForTest.id <= 3,)) == 2
        assert DummyEntityForTest.count_finished(session, filters=(DummyEntityForTest.id > 3,)) == 2
        for dummy_entity in DummyEntityForTest.get_finished(session):
            assert dummy_entity.status is None
            assert dummy_entity.edit_at is None

        for dummy_entity in DummyEntityForTest.get_finished(session, only_fields=["id", "status", "edit_at"]):
            assert dummy_entity.status is not None
            assert dummy_entity.edit_at is not None

        for dummy_entity in DummyEntityForTest.get_finished(
                session,
                only_fields=[
                    DummyEntityForTest.id,
                    DummyEntityForTest.status,
                    DummyEntityForTest.edit_at,
                ]
        ):
            assert dummy_entity.status is not None
            assert dummy_entity.edit_at is not None

        session.commit()
        session.close()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
