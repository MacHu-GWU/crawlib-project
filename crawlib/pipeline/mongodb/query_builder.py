#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

与Scheduler相关的Mongodb Query.
"""

try:
    from ...timestamp import x_seconds_before_now
    from ...status import FINISHED_STATUS_CODE
except:  # pragma: no cover
    from crawlib.timestamp import x_seconds_before_now
    from crawlib.status import FINISHED_STATUS_CODE


def finished(finished_status,
             update_interval,
             status_key,
             edit_at_key):
    """
    Create dict query for pymongo that getting all finished task.

    :param finished_status: int, status code that greater or equal than this
        will be considered as finished.
    :param update_interval: int, the record will be updated every x seconds.
    :param status_key: status code field key, support dot notation.
    :param edit_at_key: edit_at time field key, support dot notation.

    :return: dict, a pymongo filter.

    **中文文档**

    状态码大于某个值, 并且, 更新时间在最近一段时间以内.
    """
    return {
        status_key: {"$gte": finished_status},
        edit_at_key: {
            "$gte": x_seconds_before_now(update_interval),
        },
    }


def finished_50(update_interval, status_key, edit_at_key):  # pragma: no cover
    return finished(
        FINISHED_STATUS_CODE,
        update_interval, status_key, edit_at_key
    )


def unfinished(finished_status,
               update_interval,
               status_key,
               edit_at_key):
    """
    Create dict query for pymongo that getting all unfinished task.

    :param finished_status: int, status code that less than this
        will be considered as unfinished.
    :param update_interval: int, the record will be updated every x seconds.
    :param status_key: status code field key, support dot notation.
    :param edit_at_key: edit_at time field key, support dot notation.

    :return: dict, a pymongo filter.


    **中文文档**

    状态码小于某个值, 或者, 现在距离更新时间已经超过一定阈值.
    """
    return {
        "$or": [
            {status_key: {"$lt": finished_status}},
            {edit_at_key: {"$lt": x_seconds_before_now(update_interval)}},
        ]
    }


def unfinished_50(update_interval, status_key, edit_at_key):  # pragma: no cover
    return unfinished(
        FINISHED_STATUS_CODE,
        update_interval, status_key, edit_at_key,
    )
