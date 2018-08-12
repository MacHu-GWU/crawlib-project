#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .decorator import auto_decode_and_soupify
    from ..base import BaseDomainSpecifiedKlass
except:  # pragma: no cover
    from crawlib.html_parser.decorator import auto_decode_and_soupify
    from crawlib.base import BaseDomainSpecifiedKlass


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
