#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy import Spider, Request
from crawlib_doc.html_parser import html_parser
from crawlib_doc.mongo_model import State, City, Zipcode


class StateListpage(Spider):
    name = "state"

    def start_requests(self):
        url = "https://crawlib.readthedocs.io/_static/state-list.html"
        req = Request(url, callback=self.parse_state)
        yield req

    def parse_state(self, response):
        parse_result = html_parser.parse_use_mongoengine(
            response=response,
            child_class=State,
        )
        parse_result.process_item()
        self.logger.info(parse_result.item)
        yield parse_result.item


class CityListpage(Spider):
    name = "city"

    def start_requests(self):
        self.logger.info(str(State.get_all_unfinished()))
        for state in State.get_all_unfinished():
            req = Request(state.build_url(), callback=self.parse_city)
            req.meta["parent"] = state
            yield req

    def parse_city(self, response):
        parse_result = html_parser.parse_use_mongoengine(
            response=response,
            parent=response.meta["parent"],
            child_class=City,
        )
        parse_result.process_item()
        self.logger.info(parse_result.item)
        yield parse_result.item


class ZipcodeListpage(Spider):
    name = "zipcode"

    def start_requests(self):
        for city in City.get_all_unfinished():
            req = Request(city.build_url(), callback=self.parse_zipcode)
            req.meta["parent"] = city
            yield req

    def parse_zipcode(self, response):
        parse_result = html_parser.parse_use_mongoengine(
            response=response,
            parent=response.meta["parent"],
            child_class=Zipcode,
        )
        parse_result.process_item()
        self.logger.info(parse_result.item)
        yield parse_result.item
