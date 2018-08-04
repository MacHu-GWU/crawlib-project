#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy_mate

from . import query_builder
from ...status import Status


class ExtendedBase(sqlalchemy_mate.ExtendedBase):
    _settings_status_key = None
    _settings_edit_at_key = None
    _settings_finished_status = Status.S50_Finished.id
    _settings_update_interval = 365 * 24 * 60 * 60
    _settings_n_child_key = None

    @classmethod
    def get_all_unfinished(cls):
        filters = query_builder.finished(
            finished_status=cls._settings_finished_status,
            update_interval=cls._settings_update_interval,
            table=cls.__table__,
            status_key=cls.__table__.columns[cls._settings_status_key],
            edit_at_key=cls.__table__.columns[cls._settings_edit_at_key],
        )
        return cls.by_filter(filters)

    @classmethod
    def get_all_finished(cls):
        filters = query_builder.finished(
            finished_status=cls._settings_finished_status,
            update_interval=cls._settings_update_interval,
            table=cls.__table__,
            status_key=cls.__table__.columns[cls._settings_status_key],
            edit_at_key=cls.__table__.columns[cls._settings_edit_at_key],
        )
        return cls.by_filter(filters)
