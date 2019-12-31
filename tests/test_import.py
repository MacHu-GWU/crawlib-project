# -*- coding: utf-8 -*-

import pytest


def test():
    import crawlib

    _ = crawlib.Status
    _ = crawlib.StatusDetail
    _ = crawlib.BaseUrlBuilder
    _ = crawlib.resolve_arg
    _ = crawlib.decoder
    _ = crawlib.epoch
    _ = crawlib.utc_now
    _ = crawlib.create_cache
    _ = crawlib.create_cache_here
    _ = crawlib.CachedRequest
    _ = crawlib.exc
    _ = crawlib.RelationshipConfig
    _ = crawlib.Relationship
    _ = crawlib.ParseResult
    _ = crawlib.MongodbEntity
    _ = crawlib.MongodbEntitySingleStatus
    _ = crawlib.SqlEntity
    _ = crawlib.SqlEntitySingleStatus
    _ = crawlib.SqlDeclarativeBase


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
