#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib.html_parser.parser import BaseHtmlParser


class PythonOrgHtmlParser(BaseHtmlParser):
    domain = "https://www.python.org"


html_parser = PythonOrgHtmlParser()


def test_to_soup():
    html_parser.to_soup("<strong>Hello World!</strong>")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
