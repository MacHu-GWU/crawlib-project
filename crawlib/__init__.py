# -*- coding: utf-8 -*-

"""
tool set for crawler project.
"""

from ._version import __version__

__short_description__ = "tool set for crawler project."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    import scrapy

    _has_scrapy = True
except ImportError:  # pragma: no cover
    _has_scrapy = False

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
    from .decode import decoder
except ImportError:  # pragma: no cover
    pass

try:
    from .entity import (
        RelationshipConfig, Relationship, ParseResult,
        MongodbEntity, MongodbEntitySingleStatus,
    )
except ImportError:  # pragma: no cover
    pass

try:
    from .time_util import epoch, utc_now
except ImportError:  # pragma: no cover
    pass

try:
    from .cache import create_cache, create_cache_here
    from .cached_request import CachedRequest
except ImportError:  # pragma: no cover
    pass

try:
    from . import (
        exc,
    )
except ImportError:  # pragma: no cover
    pass