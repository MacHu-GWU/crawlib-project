# -*- coding: utf-8 -*-

from .base import RelationshipConfig, Relationship, ParseResult
try:
    from .mongodb import MongodbEntity, MongodbEntitySingleStatus
except ImportError:
    pass
