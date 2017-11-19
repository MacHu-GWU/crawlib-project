#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
from bs4 import BeautifulSoup

try:
    from ..base import BaseDomainSpecifiedKlass
except:  # pragma: no cover
    from crawlib.base import BaseDomainSpecifiedKlass


class SoupError(Exception):
    """
    Failed to convert html to beatifulsoup.

    **中文文档**

    html成功获得了, 但是格式有错误, 不能转化为soup。
    """


class CaptchaError(Exception):
    """
    Encounter a captcha page.

    code 403

    **中文文档**

    遭遇反爬虫验证页面。
    """


class ForbiddenError(Exception):
    """
    Banned from server.

    code 403

    **中文文档**

    被服务器禁止访问。
    """


class WrongHtmlError(Exception):
    """
    The html is not the one we desired.

    **中文文档**

    页面不是我们想要的页面。有以下几种可能:

    1. 服务器暂时连不上, 返回了404页面。
    2. 服务器要求验证码, 返回了验证码页面。
    3. 页面暂时因为各种奇怪的原因不是我们需要的页面。
    """


class ParseError(Exception):
    """Failed to parse data from html, may due to bug in your method.

    **中文文档**

    由于函数的设计失误, 解析页面信息发生了错误。
    """


class ServerSideError(Exception):
    """
    Server side problem.

    code 404

    **中文文档**

    因为服务器的缘故该页面无法正常访问, 也可能已经不存在了, 但以后可能会回来。
    """


@attr.s
class ParseResult(object):
    kwargs = attr.ib(default=attr.Factory(dict))
    data = attr.ib(default=attr.Factory(dict))
    errors = attr.ib(default=attr.Factory(dict))

    def to_dict(self):  # pragma: no cover
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
        except:  # pragma: no cover
            return BeautifulSoup(html)
