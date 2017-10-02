#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
try:
    from .url_builder import util
except:  # pragma: no cover
    from crawlib.url_builder import util


class BaseDomainSpecifiedKlassMeta(type):
    def __new__(cls, name, bases, attrs):
        klass = super(BaseDomainSpecifiedKlassMeta, cls).\
            __new__(cls, name, bases, attrs)
        klass.domain
        return klass


@six.add_metaclass(BaseDomainSpecifiedKlassMeta)
class BaseDomainSpecifiedKlass(object):
    """
    You have to:

    - define a ``domain`` class variable.
    """
    domain = None

    def __init__(self):
        self.domain = util.get_domain(self.domain)

    @property
    def domain(self):
        raise NotImplementedError("You have to define domain for UrlBuilder!")
