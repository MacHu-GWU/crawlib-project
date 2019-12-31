# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as me
import pytest

from crawlib import Status
from crawlib.entity.mongodb.entity import MongodbEntitySingleStatus
from crawlib.tests.dummy_site_crawler.mongo_backend.config_init import config
from crawlib.tests.dummy_site_crawler.mongo_backend.db import db

_ = db


class TestMongoEntity(object):
    def test_all(self):
        class DummyEntityForTest(MongodbEntitySingleStatus):
            _id = me.fields.IntField(primary_key=True)
            value = me.fields.StringField()

            CONF_UPDATE_INTERVAL = 1
            CONF_STATUS_KEY = "status"
            CONF_EDIT_AT_KEY = "edit_at"
            CONF_ONLY_FIELDS = (
                "_id",
            )

            meta = dict(
                collection="dummy_entity_for_test",
                db_alias=config.DB_DATABASE.get_value(),
            )

        # --- test SqlEntity.set_db_values() method ---
        DummyEntityForTest.col().delete_many({})
        DummyEntityForTest.smart_insert(DummyEntityForTest(_id=1, value="Alice"))

        # --- test SqlEntity.get_unfinished(), SqlEntity.get_finished() methods ---
        DummyEntityForTest.smart_insert(
            [
                DummyEntityForTest(_id=1, value="Alice", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=2, value="Bob", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=3, value="Cathy", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=4, value="David", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=5, value="Edward", edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=6, value="Frank", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
                DummyEntityForTest(_id=7, value="George", status=Status.S50_Finished.id, edit_at=datetime(2099, 1, 1)),
            ]
        )
        assert DummyEntityForTest.count_unfinished() == 3
        assert DummyEntityForTest.count_unfinished(filters={"_id": {"$lte": 3}}) == 1
        assert DummyEntityForTest.count_unfinished(filters={"_id": {"$gt": 3}}) == 2
        assert DummyEntityForTest.count_unfinished(filters={"_id": {"$gt": 3}}, limit=1) == 1
        assert [
                   entity._id
                   for entity in DummyEntityForTest.get_unfinished(order_by=["-_id", ], limit=2)
               ] == [5, 4]

        # CONF_ONLY_FIELDS taken effect
        for entity in DummyEntityForTest.get_unfinished():
            assert entity.value is None

        assert DummyEntityForTest.count_finished() == 4
        assert DummyEntityForTest.count_finished(filters={"_id": {"$lte": 3}}) == 2
        assert DummyEntityForTest.count_finished(filters={"_id": {"$gt": 3}}) == 2
        assert DummyEntityForTest.count_finished(filters={"_id": {"$gt": 3}}, limit=1) == 1
        assert [
                   entity._id
                   for entity in DummyEntityForTest.get_finished(order_by=["-_id", ], limit=2)
               ] == [7, 6]
        for entity in DummyEntityForTest.get_finished():
            assert entity.value is None


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
