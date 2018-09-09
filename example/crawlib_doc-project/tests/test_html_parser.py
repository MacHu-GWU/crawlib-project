#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib_doc.mongo_model import (
    State as StateMongo,
    City as CityMongo,
    Zipcode as ZipcodeMongo,
)
from crawlib_doc.rds_model import (
    State as StateRds,
    City as CityRds,
    Zipcode as ZipcodeRds,
)
from crawlib_doc.downloader import dl
from crawlib_doc.html_parser import html_parser, MongoengineItem, RdsItem


class TestHtmlParser(object):
    def test_parse(self):
        # state
        state = StateMongo(_id="ca")
        response = dl.get(state.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=state,
            child_class=CityMongo,
            item_class=MongoengineItem,
        )
        assert len(parse_result.item.get_child_list(1)) == 2
        for city in parse_result.item.get_child_list(1):
            assert isinstance(city, CityMongo)

        state = StateRds(_id="ca")
        response = dl.get(state.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=state,
            child_class=CityRds,
            item_class=RdsItem,
        )
        assert len(parse_result.item.get_child_list(1)) == 2
        for city in parse_result.item.get_child_list(1):
            assert isinstance(city, CityRds)

        # city
        city = CityMongo(_id="arlington")
        response = dl.get(city.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=city,
            child_class=ZipcodeMongo,
            item_class=MongoengineItem,
        )
        assert len(parse_result.item.get_child_list(1)) == 2
        for zipcode in parse_result.item.get_child_list(1):
            assert isinstance(zipcode, ZipcodeMongo)

        city = CityRds(_id="ca")
        response = dl.get(city.build_url())
        parse_result = html_parser.parse(
            response=response,
            parent=city,
            child_class=ZipcodeRds,
            item_class=RdsItem,
        )
        assert len(parse_result.item.get_child_list(1)) == 2
        for zipcode in parse_result.item.get_child_list(1):
            assert isinstance(zipcode, ZipcodeRds)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
