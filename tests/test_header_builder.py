#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib.header_builder import Headers


def test_Headers():
    headers = {
        Headers.UserAgent.KEY: Headers.UserAgent.chrome,
        Headers.Connection.KEY: Headers.Connection.keep_alive,
    }
    Headers.UserAgent.random_by_statistic()
    Headers.UserAgent.random()


test_Headers()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
