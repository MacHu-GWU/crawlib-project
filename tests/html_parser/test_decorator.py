#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from scrapy.http import Request, Response
from crawlib.html_parser import decorator
from six import string_types
from bs4 import BeautifulSoup


def test_soupify():
    html = '<div class="header">Hello</div>'
    soup = decorator.soupify(html)


def test_auto_decode_and_soupify():
    with raises(NotImplementedError):
        @decorator.auto_decode_and_soupify()
        def parse_bad_case(**kwargs):
            pass

    @decorator.auto_decode_and_soupify()
    def parse_good_case1(response, html, soup):
        assert isinstance(html, string_types)
        assert isinstance(soup, BeautifulSoup)
        div = soup.find("div")
        assert div.text == "Hello World"

    @decorator.auto_decode_and_soupify()
    def parse_good_case2(response=None, html=None, soup=None):
        assert isinstance(html, string_types)
        assert isinstance(soup, BeautifulSoup)
        div = soup.find("div")
        assert div.text == "Hello World"

    @decorator.auto_decode_and_soupify()
    def parse_good_case3(response=None, html=None, soup=None, **kwargs):
        assert isinstance(html, string_types)
        assert isinstance(soup, BeautifulSoup)
        div = soup.find("div")
        assert div.text == "Hello World"

    url = "https://www.google.com"
    response = Response(
        url=url,
        request=Request(url=url),
        body='<div class="header">Hello World</div>'.encode("utf8"),
    )

    parse_good_case1(response=response)
    parse_good_case2(response=response)
    parse_good_case3(response=response)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
