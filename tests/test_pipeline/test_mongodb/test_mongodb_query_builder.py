#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import rolex
import random
import mongomock
from datetime import datetime
from crawlib import Status
from crawlib.pipeline.mongodb import query_builder


@pytest.fixture
def col():
    client = mongomock.MongoClient()
    db = client["test"]
    col = db["test_col"]
    return col


class TestQueryBuilder(object):
    def test_finished_unfinished(self, col):
        status_key, edit_at_key = "status", "edit_at"
        col.insert([
            {
                status_key: random.randint(Status.S0_ToDo.id, Status.S99_Finalized.id),
                edit_at_key: rolex.add_hours(datetime.now(), random.randint(-48, 0))
            } for _ in range(100)
        ])

        filters = query_builder.finished(
            finished_status=50,
            update_interval=24 * 3600,
            status_key=status_key,
            edit_at_key=edit_at_key,
        )
        finished_count = col.find(filters).count()
        for doc in col.find(filters):
            status, edit_at = doc[status_key], doc[edit_at_key]
            assert status >= 50
            assert (datetime.now() - edit_at).total_seconds() <= 24 * 3600

        filters = query_builder.unfinished(
            finished_status=50,
            update_interval=24 * 3600,
            status_key=status_key,
            edit_at_key=edit_at_key,
        )
        unfinished_count = col.find(filters).count(0)
        for doc in col.find(filters):
            status, edit_at = doc[status_key], doc[edit_at_key]
            assert (status < 50) or (
                (datetime.now() - edit_at).total_seconds() > 24 * 3600)

        assert (finished_count + unfinished_count) == 100


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
