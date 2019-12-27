# -*- coding: utf-8 -*-

import pytest

from crawlib.entity.base import Entity


class Country(Entity):
    n_state = "n_state_field"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
