#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawlib import (
    BaseHtmlParser,
    OneToManyMongoEngineItem,
    OneToManyRdsItem,
    ParseResult,
    auto_decode_and_soupify,
    Status,
)

try:
    from .constant import DOMAIN
except:
    from crawlib_doc.constant import DOMAIN


class MongoengineItem(OneToManyMongoEngineItem):
    _settings_NUMBER_OF_CHILD_TYPES_required = 1
    _settings_N_CHILD_1_KEY_optional = "n_child"


MongoengineItem.validate_implementation()


class RdsItem(OneToManyRdsItem):
    _settings_NUMBER_OF_CHILD_TYPES_required = 1
    _settings_N_CHILD_1_KEY_optional = "n_child"


RdsItem.validate_implementation()


class HtmlParser(BaseHtmlParser):
    @auto_decode_and_soupify()
    def parse(self,
              response=None,
              html=None,
              soup=None,
              parent=None,
              child_class=None,
              item_class=None,
              **kwargs):
        res = ParseResult()
        if parent is None:
            parent_class = None
        else:
            parent_class = parent.__class__

        item = item_class(
            parent_class=parent_class,
            parent=parent,
            child_class_1=child_class,
        )
        res.item = item

        item.post_init()
        for a in soup.find_all("a"):
            state_city_or_zipcode = child_class(
                _id=a["href"].split(".")[0],
                name=a.text,
            )
            item.append_child(state_city_or_zipcode, nth=1)

        if item.get_n_child(nth=1) > 0:
            res.status = Status.S50_Finished.id
        else:
            res.status = Status.S40_InCompleteData.id

        return res


html_parser = HtmlParser(domain=DOMAIN)

if __name__ == "__main__":
    import requests
    from crawlib_doc.url_builder import url_builder
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

    res = html_parser.parse(
        response=requests.get(url_builder.build_state_listpage()),
        child_class=StateMongo,
        item_class=MongoengineItem,
    )
    res = html_parser.parse(
        response=requests.get(url_builder.build_state_listpage()),
        child_class=StateRds,
        item_class=RdsItem,
    )
    print(res.item)

    #
    # res = html_parser.parse(
    #     response=requests.get(url_builder.build_city_listpage("ca")),
    #     child_class=CityMongo,
    # )
    # print(res.item)
    #
    # res = html_parser.parse(
    #     response=requests.get(url_builder.build_zipcode_listpage("san-francisco")),
    #     child_class=ZipcodeMongo,
    # )
    # print(res.item)
