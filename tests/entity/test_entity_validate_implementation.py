# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from crawlib.entity.base import Entity, RelationshipConfig, Relationship


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


def test_check_subclass_implementation_goodcase1():
    class Country(Entity):
        n_state = "n_state_field"

    class State(Entity):
        n_zipcode = "n_zipcode_field"

    class Zipcode(Entity): pass

    Country.CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(State, Relationship.Option.many, "n_state"),
    ])

    State.CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(Zipcode, Relationship.Option.many, "n_zipcode"),
    ])

    Entity._validate_relationship_config()


def test_check_subclass_implementation_goodcase2():
    class ImagePage(Entity):
        id = "image_page_id"

    class ImageDownload(Entity):
        id = "image_page_id"

    ImagePage.CONF_RELATIONSHIP = RelationshipConfig([
        Relationship(ImageDownload, Relationship.Option.one, None),
    ])

    Entity._validate_relationship_config()



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
