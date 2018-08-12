#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import rolex
import random
from datetime import datetime
from crawlib import Status
from crawlib.pipeline.rds import query_builder
from sqlalchemy_mate import engine_creator


@pytest.fixture
def engine():
    return engine_creator.create_sqlite()


class TestQueryBuilder(object):
    def test_finished_unfinished(self, engine):
        from sqlalchemy import MetaData, Table, Column
        from sqlalchemy import Integer, DateTime

        status_key, edit_at_key = "status", "edit_at"

        metadata = MetaData()
        t_user = Table(
            "user", metadata,
            Column(status_key, Integer),
            Column(edit_at_key, DateTime),
        )
        metadata.create_all(engine)

        engine.execute(
            t_user.insert(),
            [
                {
                    status_key: random.randint(Status.S0_ToDo.id, Status.S99_Finalized.id),
                    edit_at_key: rolex.add_hours(datetime.now(), random.randint(-48, 0))
                } for _ in range(100)
            ],
        )

        sql = query_builder.finished(
            finished_status=50,
            update_interval=24 * 3600,
            table=t_user,
            status_column=t_user.columns[status_key],
            edit_at_column=t_user.columns[edit_at_key],
        )
        finished_count = engine.execute(sql.count()).fetchone()[0]
        for row in engine.execute(sql):
            status, edit_at = row[status_key], row[edit_at_key]
            assert status >= 50
            assert (datetime.now() - edit_at).total_seconds() <= 24 * 3600

        sql = query_builder.unfinished(
            finished_status=50,
            update_interval=24 * 3600,
            table=t_user,
            status_column=t_user.columns[status_key],
            edit_at_column=t_user.columns[edit_at_key],
        )
        unfinished_count = engine.execute(sql.count()).fetchone()[0]
        for doc in engine.execute(sql):
            status, edit_at = doc[status_key], doc[edit_at_key]
            assert (status < 50) or (
                (datetime.now() - edit_at).total_seconds() > 24 * 3600)

        assert (finished_count + unfinished_count) == 100


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
