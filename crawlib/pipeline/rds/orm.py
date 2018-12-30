#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Integer, DateTime
import sqlalchemy_mate

from . import query_builder
from ...status import Status


class ExtendedBase(sqlalchemy_mate.ExtendedBase):
    _settings_STATUS_KEY_required = None
    _settings_EDIT_AT_KEY_required = None
    _settings_FINISHED_STATUS_required = Status.S50_Finished.id
    _settings_UPDATE_INTERVAL_required = 365 * 24 * 60 * 60

    @classmethod
    def get_all_unfinished(cls, engine_or_session):
        sql = query_builder.unfinished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            table=cls.__table__,
            status_column=cls.__table__.columns[cls._settings_STATUS_KEY_required],
            edit_at_column=cls.__table__.columns[cls._settings_EDIT_AT_KEY_required],
        )
        return cls.by_sql(sql, engine_or_session)

    @classmethod
    def get_all_finished(cls, engine_or_session):
        sql = query_builder.finished(
            finished_status=cls._settings_FINISHED_STATUS_required,
            update_interval=cls._settings_UPDATE_INTERVAL_required,
            table=cls.__table__,
            status_column=cls.__table__.columns[cls._settings_STATUS_KEY_required],
            edit_at_column=cls.__table__.columns[cls._settings_EDIT_AT_KEY_required],
        )
        return cls.by_sql(sql, engine_or_session)

    @classmethod
    def validate_implementation(cls):
        if cls._settings_STATUS_KEY_required is None:
            raise NotImplementedError(
                "you has to specify `_settings_STATUS_KEY_required`!")

        try:
            status_field = cls.__table__.columns[cls._settings_STATUS_KEY_required]
            if not isinstance(status_field.type, Integer):
                raise NotImplementedError(
                    "edit at field has to be a DateTimeField field!")
        except:
            raise NotImplementedError("status field (IntField) not found!")

        if cls._settings_EDIT_AT_KEY_required is None:
            raise NotImplementedError(
                "you has to specify `_settings_EDIT_AT_KEY_required`!")

        try:
            edit_at_field = cls.__table__.columns[cls._settings_EDIT_AT_KEY_required]
            if not isinstance(edit_at_field.type, DateTime):
                raise NotImplementedError(
                    "edit at field has to be a DateTimeField field!")
        except:
            raise NotImplementedError(
                "edit at field (DateTimeField) not found!")
