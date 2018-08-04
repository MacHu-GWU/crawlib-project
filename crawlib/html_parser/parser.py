#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
from datetime import datetime
from scrapy import Item

try:
    from .decorator import auto_decode_and_soupify
    from .errors import SoupError
    from ..decode import decoder
    from ..base import BaseDomainSpecifiedKlass
    from ..status import Status
except:  # pragma: no cover
    from crawlib.html_parser.decorator import auto_decode_and_soupify
    from crawlib.html_parser.errors import SoupError
    from crawlib.decode import decoder
    from crawlib.base import BaseDomainSpecifiedKlass
    from crawlib.status import Status


class ExtendedItem(Item):
    def process(self, parse_result):
        raise NotImplementedError


@attr.s
class ParseResult(object):
    """Html Parse Result.

    :param params: parser function parameters. parser函数的所有参数.
    :param data: parsed data. 解析出的数据.
    :param log: error dictionary.
    :param status: int, status code. 抓取状态码
    :param time: datetime. 抓取的时间
    """
    params = attr.ib(default=attr.Factory(dict))
    item = attr.ib(default=None, validator=attr.validators.instance_of(Item))
    log = attr.ib(default=attr.Factory(dict))
    status = attr.ib(default=None)
    create_at = attr.ib(default=attr.Factory(datetime.now))

    _param_key = "params"
    _item_key = "data"
    _log_key = "log"
    _status_key = "status"
    _create_at_key = "create_at"

    _finished_status = Status.S50_Finished.id

    def to_dict(self):  # pragma: no cover
        return attr.asdict(self)

    def is_finished(self):
        return self.status >= self._finished_status

    def process_item(self):
        self.item.process(parse_result=self)


class BaseHtmlParser(BaseDomainSpecifiedKlass):
    """
    Html Parser is to parse

    Base Html Parser. Able to get useful data from html.
    """

    @auto_decode_and_soupify()
    def parse(self, response=None, html=None, soup=None, *kwargs):
        """
        A example parse function to extract data from html.

        How to implement this parse function:

        1. all possible exception should be captured inside a try exception
            clause.
        2. status code should be saved in ``ParseResult.status``.
        3. exception info should be saved in ``ParseResult.log``.
        4. undefined exception will be captured by the outer try exception
            clause, and it will give a ``Status.S30_ParseError.id``.
        
        .. note::

            This method is just for demonstration.

        :return: :class:`ParseResult`


        **中文**

        如何
        """
        raise NotImplementedError
