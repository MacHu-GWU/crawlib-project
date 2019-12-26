# -*- coding: utf-8 -*-

from __future__ import print_function
from ..base import DomainSpecifiedKlass
from ... import util


class BaseUrlBuilder(DomainSpecifiedKlass):
    """
    Base url builder. Provide functional interface to create url.

    Example::

        >>> from crawlib2 import BaseUrlBuilder
        >>> class PythonOrgUrlBuilder(DomainSpecifiedKlass):
        ...     domain = "https://www.python.org"
        ...
        ...     def url_downloads_page(self):
        ...         return self.join_all("downloads")
        ...
        ...     def url_release(self, version):
        ...         '''version is like "2.7.16", "3.6.8", ...'''
        ...         return self.join_all("downloads", "release", version.replace(".". ""))
        >>> url_builder = PythonOrgUrlBuilder()
    """

    def join_all(self, *parts):
        """
        Join all parts with domain. Example domain: https://www.python.org

        :rtype: list
        :param parts: Other parts, example: "/doc", "/py27"

        :rtype: str
        :return: url

        Example::

            >>> join_all("product", "iphone")
            https://www.apple.com/product/iphone
        """
        url = util.join_all(self.domain, *parts)
        return url

    def add_params(self, endpoint, params):
        """
        Combine query endpoint and params.
        """
        if not endpoint.startswith(self.domain):
            raise ValueError("%s not start with %s" % (endpoint, self.domain))
        return util.add_params(endpoint, params)
