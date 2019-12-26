# -*- coding: utf-8 -*-


class MongodbPipeline(object):
    def process_item(self, item, spider):
        item.process()
        return item
