# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

epoch = datetime(1970, 1, 1)


def utc_now():
    """
    Get current datetime in UTC, without time zone info.
    """
    return datetime.utcnow()


def x_seconds_before_now(seconds):
    """
    Get the datetime that ``x`` seconds before now.

    :type seconds: int
    :param seconds:

    :rtype: datetime
    :return:
    """
    return utc_now() - timedelta(seconds=seconds)


def x_seconds_after_now(seconds):
    """
    Get the datetime that ``y`` seconds after now.

    :type seconds: int
    :param seconds:

    :rtype: datetime
    :return:
    """
    return utc_now() + timedelta(seconds=seconds)
