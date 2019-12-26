# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from crawlib.entity.base import Relationship, RelationshipConfig, Entity


class TestRelationship(object):
    def test(self):
        class Post(object): pass

        with raises(TypeError):
            Relationship(Post, "many", "n_post")

        class Post(Entity): pass

        class PostCoverImage(Entity): pass

        with raises(ValueError):
            Relationship(Post, "bad relationship value", "n_post")

        with raises(ValueError):
            Relationship(Post, Relationship.Option.many)

        Relationship(Post, Relationship.Option.many, "n_post", recursive=True)

        Relationship(PostCoverImage, Relationship.Option.one, recursive=True)


class TestRelationshipConfig(object):
    def test(self):
        class MovieListpage(Entity): pass

        class Movie(Entity): pass

        class MovieCoverImage(Entity): pass

        class Cast(Entity): pass

        class Genre(Entity): pass

        config = RelationshipConfig([
            Relationship(Movie, Relationship.Option.many, "n_movie")
        ])
        assert config.get_relationship(Movie) == Relationship.Option.many
        assert config.get_n_child_key(Movie) == "n_movie"
        assert len(list(config.iter_recursive_child_class())) == 1

        config = RelationshipConfig([
            Relationship(MovieCoverImage, Relationship.Option.one),
            Relationship(Cast, Relationship.Option.many, "n_cast", recursive=False),
            Relationship(Genre, Relationship.Option.many, "n_genre", recursive=False),
        ])
        assert len(list(config.iter_recursive_child_class())) == 1


class TestEntity(object):
    def test_check_subclass_implementation_goodcase1(self):
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

        Entity.validate_relationship_config()

    def test_check_subclass_implementation_goodcase2(self):
        class ImagePage(Entity):
            id = "image_page_id"

        class ImageDownload(Entity):
            id = "image_page_id"

        ImagePage.CONF_RELATIONSHIP = RelationshipConfig([
            Relationship(ImageDownload, Relationship.Option.one, None),
        ])

        Entity.validate_relationship_config()


class TestParseResult(object):
    def test(self):
        pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
