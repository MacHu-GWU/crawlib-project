#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .constant import DOMAIN
    from .model import State, City, Zipcode
except:
    from crawlib_doc.constant import DOMAIN
    from crawlib_doc.model import State, City, Zipcode

import attr
from crawlib import (
    BaseHtmlParser, ParseResult, auto_decode_and_soupify, Status
)
from pymongo_mate import smart_insert
from scrapy import Item, Field


class ListpageItem(Item):
    parent_class = Field()
    parent = Field()
    child_class = Field()
    child_list = Field()
    parse_result = Field()

    def process(self):
        if self["parse_result"].is_finished():
            self["child_class"].smart_insert(self["child_list"])
        self["parse_result"]


class HtmlParser(BaseHtmlParser):
    @auto_decode_and_soupify()
    def parse(self,
              response,
              html=None,
              soup=None,
              data_model=None,
              **kwargs):
        res = ParseResult(
            params=dict(url=response.url, html=html),
            status=Status.S0_ToDo.id,
        )
        res.item = ListpageItem(

            child_class=data_model,
            child_list=list(),
            parse_result=res,
        )
        for a in soup.find_all("a"):
            state = data_model(
                _id=a["href"].split(".")[0],
                name=a.text,
            )
            res.item["item_list"].append(state)

        if len(res.item["item_list"]) > 0:
            res.status = Status.S50_Finished.id
        else:
            res.status = Status.S40_InCompleteData.id

        return res


html_parser = HtmlParser(domain=DOMAIN)

if __name__ == "__main__":
    import requests
    from crawlib_doc.url_builder import url_builder

    res = html_parser.parse(
        response=requests.get(url_builder.build_state_listpage()),
        data_model=State,
    )
    print(res.item)

    # res = html_parser.parse(
    #     response=requests.get(url_builder.build_city_listpage("ca")),
    #     data_model=City,
    # )
    # print(res.item)
    #
    # res = html_parser.parse(
    #     response=requests.get(url_builder.build_zipcode_listpage("san-francisco")),
    #     data_model=Zipcode,
    # )
    # print(res.item)

