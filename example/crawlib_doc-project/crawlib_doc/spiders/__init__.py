#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy import Spider, Request
from crawlib_doc.html_parser import html_parser, MongoengineItem, RdsItem
from crawlib_doc.rds_model import State, City, Zipcode
from crawlib_doc.rds_db import engine


class StateListpage(Spider):
    name = "state"

    def start_requests(self):
        url = "https://crawlib.readthedocs.io/_static/state-list.html"
        request = Request(url, callback=self.parse_state)
        yield request

    def parse_state(self, response):
        # self.logger.info(response.url)
        parse_result = html_parser.parse(
            response=response,
            parent=None,
            child_class=State,
            item_class=RdsItem,
        )
        parse_result.process_item(engine=engine)
        yield parse_result.item


class CityListpage(Spider):
    name = "city"

    def start_requests(self):
        for state in State.get_all_unfinished(engine):
            req = Request(state.build_url(), callback=self.parse_city)
            req.meta["parent"] = state
            yield req

    def parse_city(self, response):
        # self.logger.info(response.url)
        parse_result = html_parser.parse(
            response=response,
            parent=response.meta["parent"],
            child_class=City,
            item_class=RdsItem,
        )
        parse_result.process_item(engine=engine)
        yield parse_result.item


class ZipcodeListpage(Spider):
    name = "zipcode"

    def start_requests(self):
        for city in City.get_all_unfinished(engine):
            req = Request(city.build_url(), callback=self.parse_zipcode)
            req.meta["parent"] = city
            yield req

    def parse_zipcode(self, response):
        # self.logger.info(response.url)
        parse_result = html_parser.parse(
            response=response,
            parent=response.meta["parent"],
            child_class=Zipcode,
            item_class=RdsItem,
        )
        parse_result.process_item(engine=engine)
        yield parse_result.item
