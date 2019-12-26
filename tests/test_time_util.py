# -*- coding: utf-8 -*-

import pytest
from pytest import approx
from crawlib import time_util
from time import tzname
from datetime import datetime


def test_utc_now():
    utc_now = time_util.utc_now()
    now = datetime.now()
    delta = abs((now - utc_now).total_seconds())

    assert utc_now.tzinfo is None
    if "GMT" not in tzname:
        assert delta >= 3599
    else:
        assert delta <= 0.001


def test_before_and_after_now():
    one_hour_after_now = time_util.x_seconds_after_now(3600)
    one_hour_before_now = time_util.x_seconds_before_now(3600)

    assert (one_hour_after_now - one_hour_before_now).total_seconds() == approx(7200)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
