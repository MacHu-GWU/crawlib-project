#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from crawlib import timestamp


def test():
    assert abs(
        (timestamp.x_seconds_after_now(3600) -
         timestamp.x_seconds_before_now(3600)).total_seconds() - 7200
    ) <= 1


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
