#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
from bs4 import BeautifulSoup
try:
    from ..base import BaseDomainSpecifiedKlass
except:  # pragma: no cover
    from crawlib.base import BaseDomainSpecifiedKlass


@attr.s
class ParseResult(object):
    kwargs = attr.ib(default=attr.Factory(dict))
    data = attr.ib(default=attr.Factory(dict))
    errors = attr.ib(default=attr.Factory(dict))

    def to_dict(self):
        return attr.asdict(self)


class BaseHtmlParser(BaseDomainSpecifiedKlass):

    """
    Html Parser is to parse

    Base Html Parser. Able to get useful data from html.

    You have to:

    - define a ``domain`` class variable.
    """

    def to_soup(self, html):
        """
        Convert html to BeautifulSoup
        """
        try:
            return BeautifulSoup(html, "html.parser")
        except:
            return BeautifulSoup(html)
