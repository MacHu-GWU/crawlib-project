#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from scrapy.http import Request, Response
from crawlib.html_parser import decorator
from six import string_types
from bs4 import BeautifulSoup


def test_soupify():
    html = '<div class="header">Hello World</div>'
    soup = decorator.soupify(html)


def test_auto_decode_and_soupify():
    test_url = "https://www.google.com"
    test_html = '<div class="header">Hello World</div>'
    test_body = test_html.encode("utf8")
    test_response = Response(
        url=test_url,
        request=Request(url=test_url),
        body=test_body,
    )

    with raises(NotImplementedError):
        @decorator.auto_decode_and_soupify()
        def parse_bad_case(**kwargs):
            pass

    def _validate(html, soup):
        assert isinstance(html, string_types)
        assert isinstance(soup, BeautifulSoup)
        div = soup.find("div")
        assert div.text == "Hello World"

    @decorator.auto_decode_and_soupify()
    def parse_good_case1(response, html, soup):
        _validate(html, soup)

    @decorator.auto_decode_and_soupify()
    def parse_good_case2(response=None, html=None, soup=None):
        _validate(html, soup)

    @decorator.auto_decode_and_soupify()
    def parse_good_case3(response=None, html=None, soup=None, **kwargs):
        _validate(html, soup)

    class HtmlParser(object):
        @decorator.auto_decode_and_soupify()
        def parse_good_case4(self, response=None, html=None, soup=None, **kwargs):
            _validate(html, soup)

    html_parser = HtmlParser()

    parse_good_case1(response=test_response)
    parse_good_case2(response=test_response)
    parse_good_case3(response=test_response)

    parse_good_case2(html=test_html)
    parse_good_case3(html=test_html)

    html_parser.parse_good_case4(response=test_response)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
