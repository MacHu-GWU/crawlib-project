#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from crawlib.data_class import (
    ExtendedItem, OneToManyMongoEngineItem, ParseResult, Field,
)
from crawlib.pipeline.mongodb.orm import ExtendedDocument
from mongoengine import fields


class UserItem(ExtendedItem):
    id = Field()
    name = Field()


class TestExtendedItem(object):
    pass


class TestOneToManyMongoEngineItem(object):
    def test(self):
        # define some example
        class State(ExtendedDocument):
            _id = fields.StringField(primary_key=True)

        class City(ExtendedDocument):
            _id = fields.StringField(primary_key=True)

        class StateItem(OneToManyMongoEngineItem):
            _settings_NUMBER_OF_CHILD_TYPES_required = 1
            _settings_N_CHILD_1_KEY_optional = "n_city"

        StateItem.validate_implementation()

        # test
        state_item = StateItem(
            parent_class=State,
            parent=State(_id="ca"),
            child_class_1=City,
        )
        state_item.post_init()

        state_item.append_child(City(_id="los-angeles"), nth=1)
        state_item.append_child(City(_id="san-francisco"), nth=1)

        assert state_item.get_n_child(nth=1) == 2
        assert state_item.get_child_class(nth=1) is City
        assert len(state_item.get_child_list(nth=1)) == 2

        # parse_result = ParseResult(
        #     item=state_item,
        #     status=ParseResult._settings_finished_status,
        # )
        # state_item.process(parse_result)


class TestParseResult(object):
    def test_item_validator(self):
        # not specified, gives None
        assert ParseResult().item is None
        # use ExtendedItem
        ParseResult(item=UserItem())
        # validation failed
        with raises(TypeError):
            ParseResult(item=1)

    def test_is_finished(self):
        assert ParseResult(
            status=ParseResult._settings_FINISHED_STATUS_CODE_required) \
                .is_finished() is True
        assert ParseResult(status=0).is_finished() is False
        assert ParseResult().is_finished() is False

    def test_process_item(self):
        parse_result = ParseResult(item=UserItem(id=1, name="Alice"))
        with raises(NotImplementedError):
            parse_result.process_item()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
