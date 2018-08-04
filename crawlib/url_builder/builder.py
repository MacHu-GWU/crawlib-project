#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .. import util
    from ..base import BaseDomainSpecifiedKlass
except:  # pragma: no cover
    from crawlib import util
    from crawlib.base import BaseDomainSpecifiedKlass


class BaseUrlBuilder(BaseDomainSpecifiedKlass):
    """
    Base url builder. Provide functional interface to create url.
    """

    def join_all(self, *parts):
        """
        Join all parts with domain. Example domain: https://www.python.org

        :param parts: Other parts, example: "/doc", "/py27"
        :return: url
        """
        url = util.join_all(self.domain, *parts)
        return url

    def add_params(self, endpoint, params):
        """
        Combine query endpoint and params.
        """
        assert endpoint.startswith(self.domain)
        return util.add_params(endpoint, params)

    def build_url(self, *args, **kwargs):
        """
        An example url builder method.
        """
        raise NotImplementedError
