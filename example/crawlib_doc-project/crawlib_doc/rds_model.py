#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, String, Integer, DateTime
from crawlib import Status
from crawlib.pipeline.rds.orm import ExtendedBase

try:
    from .rds_db import engine
    from .url_builder import url_builder
except:
    from crawlib_doc.rds_db import engine
    from crawlib_doc.url_builder import url_builder

Base = declarative_base()

class Thing(ExtendedBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    _id = Column(String, primary_key=True)
    name = Column(String)
    n_child = Column(Integer)
    _status = Column(Integer, default=Status.S0_ToDo.id)
    _edit_at = Column(Integer, default=datetime(1970, 1, 1))

    _settings_STATUS_KEY_required = "_status"
    _settings_EDIT_AT_KEY_required = "_edit_at"


class State(Thing, Base):
    def build_url(self):
        return url_builder.build_city_listpage(self._id)


class City(Thing, Base):
    def build_url(self):
        return url_builder.build_zipcode_listpage(self._id)


class Zipcode(Thing, Base):
    pass


t_state = State.__table__
t_city = City.__table__
t_zipcode = Zipcode.__table__

Base.metadata.create_all(engine)
