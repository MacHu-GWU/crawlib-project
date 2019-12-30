# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from crawlib.entity.base import Entity


def test_validate_implementation():
    # validate abstract method
    class Country(Entity):
        pass

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.make_test_entity" in str(e)

    class Country(Country):
        @classmethod
        def make_test_entity(cls):
            return cls()

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.build_url" in str(e)

    class Country(Country):
        def build_url(self):
            return "http://www.example.com/{}".format(self.id)

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.build_request" in str(e)

    class Country(Country):
        def build_request(self, url, **kwargs):
            return url

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.send_request" in str(e)

    class Country(Country):
        def send_request(self, request, **kwargs):
            return "<html>Hello World</html>"

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.parse_response" in str(e)

    class Country(Country):
        def parse_response(self, url, request, response, **kwargs):
            return {"data": None}

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "Entity.process_pr" in str(e)

    # validate configuration
    class Country(Country):
        def process_pr(self, pres, **kwargs):
            pass

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "CONF_STATUS_KEY" in str(e)

    class Country(Country):
        CONF_STATUS_KEY = "status"

    with raises(NotImplementedError) as e:
        Country.validate_implementation()
    assert "CONF_EDIT_AT_KEY" in str(e)

    class Country(Country):
        CONF_EDIT_AT_KEY = "edit_at"

        @classmethod
        def _validate_orm_related(cls):
            pass

    Country.validate_implementation()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
