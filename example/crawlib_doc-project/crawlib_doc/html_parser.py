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
    from .mongo_model import Thing as ThingMongo
    from .rds_model import Thing as ThingRds
except:
    from crawlib_doc.constant import DOMAIN
    from crawlib_doc.mongo_model import Thing as ThingMongo
    from crawlib_doc.rds_model import Thing as ThingRds


class MongoengineItem(OneToManyMongoEngineItem):
    _settings_NUMBER_OF_CHILD_TYPES_required = 1
    _settings_N_CHILD_1_KEY_optional = ThingMongo.n_child.name


MongoengineItem.validate_implementation()


class RdsItem(OneToManyRdsItem):
    _settings_NUMBER_OF_CHILD_TYPES_required = 1
    _settings_N_CHILD_1_KEY_optional = ThingRds.n_child.name


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

        try:
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
        except Exception as e:
            res.log["error"] = str(e)

        return res


html_parser = HtmlParser(domain=DOMAIN)
