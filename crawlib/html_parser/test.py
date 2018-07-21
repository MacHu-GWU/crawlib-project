#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    @wrapper
    def myfunc(*args, **kwargs):
        ...

equals to::

    wrapper(myfunc)(*args, **kwargs)
"""


from bs4 import BeautifulSoup
try:
    from ..decode import decoder
except:
    from crawlib.decode import decoder


def soupify(html):
    """
    Convert html to BeautifulSoup
    """
    try:
        return BeautifulSoup(html, "html.parser")
    except:  # pragma: no cover
        return BeautifulSoup(html)


def parser_func(func):
    """
    restriction:

    - first three arguments has to be:
        1. requests.Response, should not use keyword syntax.
        2. html string.
        3. bs4.BeautifulSoup.
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        _html_parser = args[0]
        if len(args) >= 2:
            _response = args[1]
        else:
            _response = kwargs["response"]

        if _html_parser.auto_decode:
            if kwargs.get("html") is None:
                kwargs["html"] = decoder.decode(
                    _response.content, _response.url)

        html = kwargs["html"]

        if _html_parser.auto_soup:
            if kwargs.get("soup") is None:
                kwargs["soup"] = soupify(html)

        return func(*args, **kwargs)

    return wrapper


class A(object):
    def __init__(self, auto_decode=False, auto_soup=False):
        self.auto_decode = auto_decode
        self.auto_soup = auto_soup

    @parser_func
    def parse_something(self, response, html=None, soup=None, **kwargs):
        # reponse =
        # print(response, html, soup)
        print(type(html))
        print(type(soup))
        # print(soup, type(soup))
        pass


# print(isinstance(B(), A))

a = A(auto_decode=True, auto_soup=True)
import requests
response = requests.get("https://www.python.org/")
a.parse_something(response=response, html=response.text)
a.parse_something(response, response.text)

