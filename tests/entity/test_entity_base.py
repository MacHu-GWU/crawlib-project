# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
from pytest import raises

from crawlib.entity.base import Relationship, RelationshipConfig, Entity, ParseResult


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


class TestParseResult(object):
    def test_init_validator(self):
        pr = ParseResult()
        assert isinstance(pr.children, list)
        assert isinstance(pr.additional_data, dict)
        assert isinstance(pr.status, int)
        assert isinstance(pr.edit_at, datetime)

        with raises(TypeError) as e:
            ParseResult(entity_data=[1, 2, 3])
        assert "ParseResult.entity_data" in str(e)

        with raises(TypeError) as e:
            ParseResult(children=[1, 2, 3])
        assert "ParseResult.children" in str(e)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
