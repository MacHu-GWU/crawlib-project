#!/usr/bin/env python
# -*- coding: utf-8 -*-

# def process_one(doc, status_key, edit_at_key):
#
#
#     doc.update()


# if res.data is None:
#
#
# def process_parse_result(res, lambda_func, status_key, edit_at_key):
#     single_data = lambda_func(res)
#     setattr(single_data, status_key, res.status)
#     setattr(single_data, edit_at_key, res.create_at)
#     single_data.col()
#
#     # list_data = lambda_func

from scrapy import Item, Field

import attr

@attr.s
class OneToOneItem(object):
    parent_model = attr.ib()
    parent_item = attr.ib()
    child1_model = attr.ib()
    child1_item_list = attr.ib(default=attr.Factory(list))
    child2_model2 = attr.ib()
    child2_item_list = attr.ib(default=attr.Factory(list))
    child3_model = attr.ib()
    child3_item_list = attr.ib(default=attr.Factory(list))

    def process(self, parse_result):
        if parse_result.is_finished():
            dct = self.parent_item.to_dict()
            dct[self.parent_item.status_key] = parse_result.status
            dct[self.parent_item.edit_at_key] = parse_result.create_at
            dct[self.parent_item.]






