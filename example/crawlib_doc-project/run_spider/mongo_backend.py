#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
use mongodb as backend.
"""

from crawlib import execute_one_to_many_job
from crawlib_doc.html_parser import html_parser, MongoengineItem
from crawlib_doc.mongo_model import State, City, Zipcode
from crawlib_doc.downloader import dl
from crawlib_doc.logger import logger


def test_state_listpage():
    url = "https://crawlib.readthedocs.io/_static/state-list.html"
    response = dl.get(url)
    parse_result = html_parser.parse(
        response=response,
        child_class=State,
        item_class=MongoengineItem,
    )
    parse_result.process_item()


test_state_listpage()


def test_city_listpage():
    execute_one_to_many_job(
        parent_class=State,
        parser_func=html_parser.parse,
        parser_func_kwargs=dict(child_class=City, item_class=MongoengineItem),
        downloader_func=dl.get,
        downloader_func_kwargs=dict(timeout=5),
        logger=logger,
        sleep_time=1,
    )


test_city_listpage()


def test_zipcode_listpage():
    execute_one_to_many_job(
        parent_class=City,
        parser_func=html_parser.parse,
        parser_func_kwargs=dict(child_class=Zipcode, item_class=MongoengineItem),
        downloader_func=dl.get,
        downloader_func_kwargs=dict(timeout=5),
        logger=logger,
        sleep_time=1,
    )


test_zipcode_listpage()


def print_result():
    for state in State.objects():
        print(state)
    for city in City.objects():
        print(city)
    for zipcode in Zipcode.objects():
        print(zipcode)


print_result()
