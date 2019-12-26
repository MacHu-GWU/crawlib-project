# -*- coding: utf-8 -*-

from .. import util


class DomainSpecifiedKlass(object):
    """
    """
    domain = None

    def __init__(self, domain=None):
        """
        :type domain: str
        :param domain:
        """
        if domain is not None:
            self.domain = domain
        if self.domain is None:
            raise ValueError("You have to specify `domain`")
        self.domain = util.get_domain(self.domain)
