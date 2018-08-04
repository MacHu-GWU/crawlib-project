#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ExtendedItem(Item):
    mongo_model = None

    def to_mongoengine_obj(self):
        return self.to_me_obj()

    def to_me_obj(self):
        return self.mongo_model(**dict(self))


def item_class_factory(name, document_model):
    attrs = {name: Field() for name in document_model._fields_ordered}
    attrs["mongo_model"] = document_model
    return type(name, (ExtendedItem,), attrs)
