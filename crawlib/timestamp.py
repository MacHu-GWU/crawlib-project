#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

epoch = datetime(1970, 1, 1)


def x_seconds_before_now(seconds):
    return datetime.now() - timedelta(seconds=seconds)


def x_seconds_after_now(seconds):
    return datetime.now() + timedelta(seconds=seconds)
