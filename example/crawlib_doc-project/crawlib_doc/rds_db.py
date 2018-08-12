#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib_mate import Path
from sqlalchemy_mate import engine_creator

dbpath = Path(__file__).parent.change(new_basename="crawlib.sqlite").abspath


def create_in_memory():
    return engine_creator.create_sqlite()


def create_local_file():
    return engine_creator.create_sqlite(dbpath)


# engine = create_in_memory()
engine = create_local_file()
