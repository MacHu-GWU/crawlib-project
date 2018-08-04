#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import select, and_, or_

try:
    from ...timestamp import x_seconds_before_now
    from ...status import FINISHED_STATUS_CODE
except:
    from crawlib.timestamp import x_seconds_before_now
    from crawlib.status import FINISHED_STATUS_CODE


def finished(finished_status,
             update_interval,
             table,
             status_column,
             edit_at_column):
    """
    Create text sql statement query for sqlalchemy that getting all finished task.

    :param finished_status: int, status code that greater or equal than this
        will be considered as finished.
    :param update_interval: int, the record will be updated every x seconds.

    :return: sqlalchemy text sql statement.

    **中文文档**

    状态码大于某个值, 并且, 更新时间在最近一段时间以内.
    """
    sql = select([table]).where(
        and_(*[
            status_column >= finished_status,
            edit_at_column >= x_seconds_before_now(update_interval)
        ])
    )
    return sql


def finished_50(update_interval,
                table,
                status_column,
                edit_at_column):
    return finished(
        FINISHED_STATUS_CODE,
        update_interval, table, status_column, edit_at_column,
    )


def unfinished(finished_status,
               update_interval,
               table,
               status_column,
               edit_at_column):
    """
    Create text sql statement query for sqlalchemy that getting all unfinished task.

    :param finished_status: int, status code that less than this
        will be considered as unfinished.
    :param update_interval: int, the record will be updated every x seconds.

    :return: sqlalchemy text sql statement.


    **中文文档**

    状态码小于某个值, 或者, 现在距离更新时间已经超过一定阈值.
    """
    sql = select([table]).where(
        or_(*[
            status_column < finished_status,
            edit_at_column < x_seconds_before_now(update_interval)
        ])
    )
    return sql


def unfinished_50(update_interval,
                  table,
                  status_column,
                  edit_at_column):
    return unfinished(
        FINISHED_STATUS_CODE,
        update_interval, table, status_column, edit_at_column,
    )
