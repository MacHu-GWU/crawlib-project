#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from crawlib import _has_scrapy
from crawlib.html_parser import decorator
from six import string_types
from bs4 import BeautifulSoup


def test_soupify():
    html = '<div class="header">Hello World</div>'
    soup = decorator.soupify(html)


# ---
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


class TestAutoDecodeAndSoupify(object):
    test_url = "https://www.python.org"
    test_html = '<div class="header">Hello World</div>'
    test_body = test_html.encode("utf8")

    def run_parse_function(self, response):
        parse_good_case1(response=response)
        parse_good_case2(response=response)
        parse_good_case3(response=response)

        parse_good_case2(html=self.test_html)
        parse_good_case3(html=self.test_html)

        html_parser.parse_good_case4(response=response)

    def test_with_requests(self):
        from requests import Response as RequestsResponse
        test_response = RequestsResponse()
        test_response.url = self.test_url
        test_response._content = self.test_body
        self.run_parse_function(test_response)

    def test_with_scrapy(self):
        if _has_scrapy:
            from scrapy.http import Request, Response

            test_response = Response(
                url=self.test_url,
                request=Request(url=self.test_url),
                body=self.test_body,
            )
            self.run_parse_function(test_response)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
