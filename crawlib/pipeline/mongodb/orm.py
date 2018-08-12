#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine_mate

from . import query_builder
from ...status import Status


class ExtendedDocument(mongoengine_mate.ExtendedDocument):
    _settings_STATUS_KEY_required = None
    _settings_EDIT_AT_KEY_required = None
    _settings_FINISHED_STATUS_required = Status.S50_Finished.id
    _settings_UPDATE_INTERVAL_required = 365 * 24 * 60 * 60

    meta = {
        "abstract": True,
    }

    @classmethod
    def get_all_unfinished(cls):
        filters = query_builder.unfinished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            status_key=cls._settings_STATUS_KEY_required,
            edit_at_key=cls._settings_EDIT_AT_KEY_required,
        )
        return cls.by_filter(filters)

    @classmethod
    def get_all_finished(cls):
        filters = query_builder.finished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            status_key=cls._settings_STATUS_KEY_required,
            edit_at_key=cls._settings_EDIT_AT_KEY_required,
        )
        return cls.by_filter(filters)


ExtendedDocument.__doc__ = mongoengine_mate.ExtendedDocument.__doc__
