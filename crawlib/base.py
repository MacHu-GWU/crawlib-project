#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from . import util
except:  # pragma: no cover
    from crawlib import util


class BaseDomainSpecifiedKlass(object):
    """
    """
    def __init__(self, domain):
        self.domain = util.get_domain(domain)
