#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
There are three major popular libraries widely used for making
http request:

- ``requests``: http://docs.python-requests.org/en/master/
- ``scrapy``: https://doc.scrapy.org/en/latest/topics/request-response.html
- ``selenium``: http://selenium-python.readthedocs.io/index.html

And there are two major popular library widely used for extracting data
from html:

- ``beautifulsoup4``: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- ``scrapy.selector``: https://doc.scrapy.org/en/latest/topics/selectors.html

This module bridge the gap.
"""

import inspect
from bs4 import BeautifulSoup
from scrapy.http import Response as ScrapyResponse
from requests import Response as RequestsResponse

from ..decode import decoder
from .errors import DecodeError, SoupError


def soupify(html):
    """
    Convert html to BeautifulSoup. It solves api change in bs4.3.
    """
    try:
        return BeautifulSoup(html, "html.parser")
    except Exception as e:  # pragma: no cover
        raise SoupError(str(e))


def access_binary(response):
    if isinstance(response, ScrapyResponse):
        binary = response.body
    elif isinstance(response, RequestsResponse):
        binary = response.content
    else:
        raise TypeError("It only support ScrapyResponse or RequestsResponse!")
    return binary


_auto_decode_and_soupify_implementation_ok_mapper = dict()


def validate_implementation_for_auto_decode_and_soupify(func):
    """
    Validate that :func:`auto_decode_and_soupify` is applicable to this
    function. If not applicable, a ``NotImplmentedError`` will be raised.
    """
    arg_spec = inspect.getargspec(func)
    for arg in ["response", "html", "soup"]:
        if arg not in arg_spec.args:
            raise NotImplementedError(
                ("{func} method has to take the keyword syntax input: "
                 "{arg}").format(func=func, arg=arg)
            )


def auto_decode_and_soupify(encoding=None, errors=decoder.ErrorsHandle.strict):
    """
    This decorator assume that there are three argument in keyword syntax:

    - ``response``: ``requests.Response`` or ``scrapy.http.Reponse``
    - ``html``: html string
    - ``soup``: ``bs4.BeautifulSoup``

    1. if ``soup`` is not available, it will automatically be generated from
        ``html``.
    2. if ``html`` is not available, it will automatically be generated from
        ``response``.

    Usage::

        @auto_decode_and_soupify()
        def parse(response, html, soup):
            ...

    **中文文档**

    此装饰器会自动检测函数中名为 ``response``, ``html``, ``soup`` 的参数, 并在
    ``html``, ``soup`` 未给出的情况下, 自动生成所期望的值. 被此装饰器装饰的函数必须
    要有以上提到的三个参数. 并且在使用时, 必须使用keyword的形式进行输入.
    """

    def deco(func):
        func_hash = hash(func)
        if not _auto_decode_and_soupify_implementation_ok_mapper \
                .get(func_hash, False):
            validate_implementation_for_auto_decode_and_soupify(func)
            _auto_decode_and_soupify_implementation_ok_mapper[func_hash] = True

        def wrapper(*args, **kwargs):
            try:
                response = kwargs.get("response")
                html = kwargs.get("html")
                soup = kwargs.get("soup")
            except KeyError as e:
                raise KeyError(
                    ("{func} method has to take the keyword syntax input: "
                     "{e}").format(func=func, e=e)
                )

            if html is None:
                binary = access_binary(response)
                try:
                    html = decoder.decode(
                        binary=binary,
                        url=response.url,
                        encoding=encoding,
                        errors=errors,
                    )
                except Exception as e:
                    raise DecodeError(str(e))
                kwargs["html"] = html

            if soup is None:
                soup = soupify(html)
                kwargs["soup"] = soup

            return func(*args, **kwargs)

        return wrapper

    return deco
