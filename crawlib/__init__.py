# -*- coding: utf-8 -*-

"""
Package Description.
"""

from ._version import __version__

__short_description__ = "Package short description."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .status import Status, StatusDetail
except ImportError:  # pragma: no cover
    pass

try:
    from .middleware.url_builder import BaseUrlBuilder
except ImportError:  # pragma: no cover
    pass

try:
    from .decorator import resolve_arg
except ImportError:  # pragma: no cover
    pass

try:
    from .entity import (
        RelationshipConfig, Relationship, ParseResult,
        MongodbEntity, MongodbEntitySingleStatus,
    )
except ImportError:  # pragma: no cover
    pass
