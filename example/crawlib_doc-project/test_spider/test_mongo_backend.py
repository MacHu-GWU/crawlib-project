#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawlib_doc.html_parser import html_parser, MongoengineItem
from crawlib_doc.mongo_model import State, City, Zipcode
import requests


def test_state_listpage():
    url = "https://crawlib.readthedocs.io/_static/state-list.html"
    response = requests.get(url)
    parse_result = html_parser.parse(
        response=response,
        child_class=State,
        item_class=MongoengineItem,
    )
    parse_result.process_item()

# test_state_listpage()


def test_city_listpage():
    for state in State.get_all_unfinished():
        response = requests.get(state.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=state,
            child_class=City,
            item_class=MongoengineItem,
        )
        parse_result.process_item()

# test_city_listpage()


def test_zipcode_listpage():
    for city in City.get_all_unfinished():
        response = requests.get(city.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=city,
            child_class=Zipcode,
            item_class=MongoengineItem,
        )
        parse_result.process_item()

# test_zipcode_listpage()