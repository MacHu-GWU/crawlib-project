#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine_mate
from mongoengine import fields

from . import query_builder
from ...status import Status
from ...timestamp import epoch


class ExtendedDocument(mongoengine_mate.ExtendedDocument):
    _settings_STATUS_KEY_required = None
    _settings_EDIT_AT_KEY_required = None
    _settings_FINISHED_STATUS_required = Status.S50_Finished.id
    _settings_UPDATE_INTERVAL_required = 365 * 24 * 60 * 60

    meta = {
        "abstract": True,
    }

    @classmethod
    def get_all_unfinished(cls, filters=None):  # pragma: no cover
        status_filters = query_builder.unfinished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            status_key=cls._settings_STATUS_KEY_required,
            edit_at_key=cls._settings_EDIT_AT_KEY_required,
        )
        if filters is not None:
            status_filters.update(filters)
        return cls.by_filter(status_filters)

    @classmethod
    def get_all_finished(cls, filters=None):  # pragma: no cover
        status_filters = query_builder.finished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            status_key=cls._settings_STATUS_KEY_required,
            edit_at_key=cls._settings_EDIT_AT_KEY_required,
        )
        if filters is not None:
            status_filters.update(filters)
        return cls.by_filter(status_filters)


ExtendedDocument.__doc__ = mongoengine_mate.ExtendedDocument.__doc__


class ExtendedDocumentSingleStatus(ExtendedDocument):
    status = fields.IntField(default=Status.S0_ToDo.id)
    edit_at = fields.DateTimeField(default=epoch)

    _settings_STATUS_KEY_required = "status"
    _settings_EDIT_AT_KEY_required = "edit_at"

    meta = {
        "abstract": True,
    }


ExtendedDocumentSingleStatus.__doc__ = mongoengine_mate.ExtendedDocument.__doc__
