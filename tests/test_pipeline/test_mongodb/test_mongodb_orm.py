#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mongoengine import connect, fields

import rolex
import random
from datetime import datetime
from crawlib.status import Status
from crawlib.pipeline.mongodb import ExtendedDocument, ExtendedDocumentSingleStatus

dbname = "devtest"
try:
    client = connect(db=dbname, alias=dbname, serverSelectionTimeoutMS=1)
    client.server_info()
    has_local_mongo = True
except:
    has_local_mongo = False


class User(ExtendedDocumentSingleStatus):
    _id = fields.IntField(primary_key=1)

    _settings_UPDATE_INTERVAL_required = 24 * 3600

    meta = {
        "db_alias": dbname,
    }


class TestMongodbOrm(object):
    def test_validation_implemented(self):
        class A(ExtendedDocument):
            pass

        with pytest.raises(NotImplementedError):
            A.validate_implementation()

        class B(ExtendedDocument):
            _settings_STATUS_KEY_required = "status"
            _settings_EDIT_AT_KEY_required = "edit_at"

        with pytest.raises(NotImplementedError):
            B.validate_implementation()

        class C(ExtendedDocument):
            status = fields.IntField()
            edit_at = fields.DateTimeField()

            _settings_STATUS_KEY_required = "status"
            _settings_EDIT_AT_KEY_required = "edit_at"

        C.validate_implementation()

    def test(self):
        if has_local_mongo is False:
            return

        data = [
            User(
                _id=_id,
                status=random.randint(
                    Status.S0_ToDo.id, Status.S99_Finalized.id),
                edit_at=rolex.add_hours(
                    datetime.now(), random.randint(-48, 0)),
            )
            for _id in range(1, 1 + 100)
        ]
        User.smart_insert(data)

        for user in User.get_all_finished(filters={"_id": {"$gt": 50}}):
            assert user._id > 50
            assert user.status >= User._settings_FINISHED_STATUS_required
            assert (datetime.now(
            ) - user.edit_at).total_seconds() <= User._settings_UPDATE_INTERVAL_required

        for user in User.get_all_unfinished(filters={"_id": {"$lte": 50}}):
            assert user._id <= 50
            assert (user.status < User._settings_FINISHED_STATUS_required) \
                   or ((datetime.now() - user.edit_at).total_seconds() > User._settings_UPDATE_INTERVAL_required)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
