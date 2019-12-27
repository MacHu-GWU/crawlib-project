# -*- coding: utf-8 -*-

import pytest
import rolex
import random
import mongomock
from datetime import datetime
from crawlib.status import Status
from crawlib.entity.mongodb import query_builder


@pytest.fixture
def col():
    client = mongomock.MongoClient()
    db = client["test"]
    col = db["test_col"]
    return col


class TestQueryBuilder(object):
    def test_finished_unfinished(self, col):
        finished_status = 50
        update_interval = 24 * 3600  # 24 hours
        status_key = "status"
        edit_at_key = "edit_at"
        n_documents = 100

        col.insert([
            {
                status_key: random.randint(Status.S0_ToDo.id, Status.S99_Finalized.id),
                edit_at_key: rolex.add_seconds(datetime.utcnow(), -random.randint(0, update_interval * 2))
            } for _ in range(n_documents)
        ])

        # test query_builder.finished
        filters = query_builder.finished(
            finished_status=finished_status,
            update_interval=update_interval,
            status_key=status_key,
            edit_at_key=edit_at_key,
        )
        finished_count = col.find(filters).count()
        for doc in col.find(filters):
            status, edit_at = doc[status_key], doc[edit_at_key]
            assert status >= finished_status
            assert (datetime.utcnow() - edit_at).total_seconds() <= update_interval

        # test query_builder.unfinished
        filters = query_builder.unfinished(
            finished_status=finished_status,
            update_interval=update_interval,
            status_key=status_key,
            edit_at_key=edit_at_key,
        )
        unfinished_count = col.find(filters).count()
        for doc in col.find(filters):
            status, edit_at = doc[status_key], doc[edit_at_key]
            assert (status < finished_status) \
                   or ((datetime.utcnow() - edit_at).total_seconds() > update_interval)

        # test if total is ``n_documents``
        assert (finished_count + unfinished_count) == n_documents


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
