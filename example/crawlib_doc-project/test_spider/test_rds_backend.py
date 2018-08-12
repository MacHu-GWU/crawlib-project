#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawlib_doc.html_parser import html_parser, RdsItem
from crawlib_doc.rds_model import State, City, Zipcode, engine
import requests


def test_state_listpage():
    url = "https://crawlib.readthedocs.io/_static/state-list.html"
    response = requests.get(url)
    parse_result = html_parser.parse(
        response=response,
        child_class=State,
        item_class=RdsItem,
    )
    parse_result.process_item(engine=engine)


# test_state_listpage()


def test_city_listpage():
    for state in State.get_all_unfinished(engine):
        response = requests.get(state.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=state,
            child_class=City,
            item_class=RdsItem,
        )
        parse_result.process_item(engine=engine)


# test_city_listpage()

def test_zipcode_listpage():
    for city in City.get_all_unfinished(engine):
        response = requests.get(city.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=city,
            child_class=Zipcode,
            item_class=RdsItem,
        )
        parse_result.process_item(engine=engine)

# test_zipcode_listpage()
