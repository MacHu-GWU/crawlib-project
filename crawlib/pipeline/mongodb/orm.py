#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import mongoengine_mate

from . import query_builder
from ...status import Status


class ExtendedDocument(mongoengine_mate.ExtendedDocument):
    _settings_status_key = None
    _settings_edit_at_key = None
    _settings_finished_status = Status.S50_Finished.id
    _settings_update_interval = 365 * 24 * 60 * 60

    meta = {
        "abstract": True,
    }

    def to_dict(self, include_none=True):
        """
        Convert to dict.

        :param include_none: bool, if False, None value field will be removed.
        """
        if include_none:
            return dict(self.items())
        else:
            return {
                key: value
                for key, value in self.items()
                if value is not None
            }

    def to_OrderedDict(self, include_none=True):
        """
        Convert to OrderedDict.

        :param include_none: bool, if False, None value field will be removed.
        """
        if include_none:
            return OrderedDict(self.items())
        else:
            return OrderedDict([
                (key, value)
                for key, value in self.items()
                if value is not None
            ])

    @classmethod
    def get_all_unfinished(cls):
        filters = query_builder.unfinished(
            finished_status=cls._settings_finished_status,
            update_interval=cls._settings_update_interval,
            status_key=cls._settings_status_key,
            edit_at_key=cls._settings_edit_at_key,
        )
        return cls.by_filter(filters)

    @classmethod
    def get_all_finished(cls):
        filters = query_builder.finished(
            finished_status=cls._settings_finished_status,
            update_interval=cls._settings_update_interval,
            status_key=cls._settings_status_key,
            edit_at_key=cls._settings_edit_at_key,
        )
        return cls.by_filter(filters)


ExtendedDocument.__doc__ = mongoengine_mate.ExtendedDocument.__doc__
