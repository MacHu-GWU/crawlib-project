# -*- coding: utf-8 -*-

"""
**中文文档**

与Scheduler相关的Mongodb Query.
"""

from functools import partial
from ...time_util import x_seconds_before_now
from ...status import FINISHED_STATUS_CODE


def unfinished(finished_status,
               update_interval,
               status_key,
               edit_at_key):
    """
    Create dict query for pymongo to get all **UNFINISHED** task.

    :type finished_status: int
    :param finished_status: status code that less than this
        will be considered as unfinished.

    :type update_interval: int
    :param update_interval: the record will be updated every x seconds.

    :type status_key: str
    :param status_key: status code field key, support dot notation.

    :type edit_at_key: str
    :param edit_at_key: edit_at time field key, support dot notation.

    :return: dict, a pymongo filter.

    **中文文档**

    获得被视为所有未完成的文档. 条件是: 状态码小于 ``已完成标记`` 的设定值,
        或者现在离最近一次的更新时间, 已经超过一定阈值, 是时候该更新了.
    """
    return {
        "$or": [
            {status_key: {"$lt": finished_status}},
            {edit_at_key: {"$lt": x_seconds_before_now(update_interval)}},
        ]
    }


def finished(finished_status,
             update_interval,
             status_key,
             edit_at_key):
    """
    Create dict query for pymongo to get all **FINISHED** task.

    :type finished_status: int
    :param finished_status: status code that less than this
        will be considered as unfinished.

    :type update_interval: int
    :param update_interval: the record will be updated every x seconds.

    :type status_key: str
    :param status_key: status code field key, support dot notation.

    :type edit_at_key: str
    :param edit_at_key: edit_at time field key, support dot notation.

    **中文文档**

    获得被视为所有已完成的文档. 条件是: 状态码大于等于 ``已完成标记`` 的设定值,
        并且现在离最近一次的更新时间, 未超过设定阈值, 还不需要更新了.
    """
    return {
        status_key: {"$gte": finished_status},
        edit_at_key: {
            "$gte": x_seconds_before_now(update_interval),
        },
    }


unfinished_50 = partial(unfinished, finished_status=FINISHED_STATUS_CODE)
finished_50 = partial(finished, finished_status=FINISHED_STATUS_CODE)
