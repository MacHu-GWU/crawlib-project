#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
use relational database as backend.
"""

from crawlib import execute_one_to_many_job
from crawlib_doc.html_parser import html_parser, RdsItem
from crawlib_doc.rds_model import State, City, Zipcode
from crawlib_doc.downloader import dl
from crawlib_doc.logger import logger
from crawlib_doc.rds_db import engine
from sqlalchemy.orm import sessionmaker


def test_state_listpage():
    url = "https://crawlib.readthedocs.io/_static/state-list.html"
    response = dl.get(url)
    parse_result = html_parser.parse(
        response=response,
        child_class=State,
        item_class=RdsItem,
    )
    parse_result.process_item(engine=engine)


test_state_listpage()


def test_city_listpage():
    execute_one_to_many_job(
        parent_class=State,
        get_unfinished_kwargs=dict(engine_or_session=engine),
        parser_func=html_parser.parse,
        parser_func_kwargs=dict(child_class=City, item_class=RdsItem),
        downloader_func=dl.get,
        downloader_func_kwargs=dict(timeout=5),
        process_item_func_kwargs=dict(engine=engine),
        logger=logger,
        sleep_time=1,
    )


test_city_listpage()


def test_zipcode_listpage():
    execute_one_to_many_job(
        parent_class=City,
        get_unfinished_kwargs=dict(engine_or_session=engine),
        parser_func=html_parser.parse,
        parser_func_kwargs=dict(child_class=Zipcode, item_class=RdsItem),
        downloader_func=dl.get,
        downloader_func_kwargs=dict(timeout=5),
        process_item_func_kwargs=dict(engine=engine),
        logger=logger,
        sleep_time=1,
    )


test_zipcode_listpage()


def print_result():
    ses = sessionmaker(bind=engine)()
    for state in ses.query(State):
        print(state)
    for city in ses.query(City):
        print(city)
    for zipcode in ses.query(Zipcode):
        print(zipcode)
    ses.close()


print_result()
