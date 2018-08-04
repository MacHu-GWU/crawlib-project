#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy import Spider, Request
from crawlib_doc.html_parser import html_parser, ParseResult
from crawlib_doc.model import State, City, Zipcode
from crawlib.pipeline import mongodb


class StateListpage(Spider):
    name = "state"

    def start_requests(self):
        url = "https://crawlib.readthedocs.io/_static/state-list.html"
        yield Request(url, callback=self.parse_state)

    def parse_state(self, response):
        res = html_parser.parse(response, data_model=State)
        res.item.process()
        self.logger.info(res.item)
        yield res.item


class CityListpage(Spider):
    name = "city"

    def start_requests(self):
        self.logger.info(str(State.get_all_unfinished()))
        for state in State.get_all_unfinished():
            yield Request(state.build_url(), callback=self.parse_city)

    def parse_city(self, response):
        res = html_parser.parse(response, data_model=City)
        res.item.process()
        self.logger.info(res.item)
        yield res.item


class ZipcodeListpage(Spider):
    name = "zipcode"

    def start_requests(self):
        for city in City.get_all_unfinished():
            yield Request(city.build_url(), callback=self.parse_zipcode)

    def parse_zipcode(self, response):
        res = html_parser.parse(response, data_model=Zipcode)
        res.item.process()
        self.logger.info(res.item)
        yield res.item
