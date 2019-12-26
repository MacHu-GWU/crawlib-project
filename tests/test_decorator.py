# -*- coding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup
from pytest import raises
from requests import Response as RequestResponse
from requests_html import HTML
from scrapy.http import Request as ScrapyRequest, Response as ScrapyResponse
from six import string_types

from crawlib import decorator


def test_soupify():
    html = '<div class="header">Hello World</div>'
    decorator.soupify(html)


def test_validate_func_implementation():
    def parse_html_func(**kwargs): pass

    with raises(NotImplementedError):
        decorator.validate_func_def(parse_html_func)

    def parse_html_func(response=None, **kwargs): pass

    with raises(NotImplementedError):
        decorator.validate_func_def(parse_html_func)

    def parse_html_func(response=None, html=None, **kwargs): pass

    decorator.validate_func_def(parse_html_func)

    def parse_html_func(response=None, html="<html></html>", **kwargs): pass

    with raises(NotImplementedError):
        decorator.validate_func_def(parse_html_func)

    def parse_html_func(response=None, html=None, soup=None, rhtml=None, **kwargs): pass

    with raises(NotImplementedError):
        decorator.validate_func_def(parse_html_func)


def validate_resolved_arg(html=None, soup=None, rhtml=None):
    assert isinstance(html, string_types)
    if soup is not None:
        assert isinstance(soup, BeautifulSoup)
        div = soup.find("div", class_="title")
        assert div.text == "Hello World"
    if rhtml is not None:
        assert isinstance(rhtml, HTML)
        assert rhtml.xpath("/html/div[@class='title']")[0].text == "Hello World"


class TestDecorator(object):
    url = "https://www.python.org"
    content = b'<html><div class="title">Hello World</div></html>'
    html = str(content)
    response_requests = None
    response_scrapy = None

    @classmethod
    def setup_class(cls):
        cls.response_requests = RequestResponse()
        cls.response_requests.url = cls.url
        cls.response_requests._content = cls.content
        cls.response_scrapy = ScrapyResponse(
            url=cls.url,
            request=ScrapyRequest(url=cls.url),
            body=cls.content,
        )

    def test_resolve_arg(self):
        @decorator.resolve_arg(
            response_arg="new_response",
            html_arg="new_html",
            soup_arg="new_soup",
        )
        def parse_html_func_with_soup(new_response=None, new_html=None, new_soup=None, **kwargs):
            validate_resolved_arg(html=new_html, soup=new_soup)

        parse_html_func_with_soup(new_response=self.response_requests)
        parse_html_func_with_soup(new_response=self.response_scrapy)
        parse_html_func_with_soup(new_html=self.html)

        @decorator.resolve_arg(
            response_arg="new_response",
            html_arg="new_html",
            rhtml_arg="new_rhtml",
        )
        def parse_html_func_with_rhtml(new_response=None, new_html=None, new_rhtml=None, **kwargs):
            validate_resolved_arg(html=new_html, rhtml=new_rhtml)

        parse_html_func_with_rhtml(new_response=self.response_requests)
        parse_html_func_with_rhtml(new_response=self.response_scrapy)
        parse_html_func_with_rhtml(new_html=self.html)

        class HtmlParser(object):
            @decorator.resolve_arg()
            def parse_html(self, response=None, html=None, soup=None, **kwargs):
                validate_resolved_arg(html=html, soup=soup)

        html_parser = HtmlParser()
        html_parser.parse_html(response=self.response_requests)
        html_parser.parse_html(response=self.response_scrapy)
        html_parser.parse_html(html=self.html)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
