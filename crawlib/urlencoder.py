#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests.compat import urlparse, urljoin


class BaseUrlEncoder(object):

    """Base Url Encoder. Provide functional interface to create url.
    """
    domain = None
    
    def __init__(self):
        result = urlparse(self.domain)
        self.domain = "%s://%s" % (result.scheme, result.netloc)        
    
    def join(self, *parts):
        return urljoin(self.domain, *parts)

    def get_url(self, *args, **kwargs):
        """An example method, takes argument and return url.
        """
        return self.domain


if __name__ == "__main__":
    def test_urlencoder():
        class PythonOrgUrlEncoder(BaseUrlEncoder):
            domain = "https://www.python.org"

        urlencoder = PythonOrgUrlEncoder()
        assert urlencoder.join("/about/") == "https://www.python.org/about/"

    test_urlencoder()
