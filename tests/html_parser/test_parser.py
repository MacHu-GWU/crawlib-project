#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib.html_parser.parser import ExtendedItem, ParseResult, BaseHtmlParser

if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
