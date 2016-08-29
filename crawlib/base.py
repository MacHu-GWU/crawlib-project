#!/usr/bin/env python
# -*- coding: utf-8 -*-


class HtmlParser(object):
    """Base Html Parser. Able to get useful data from html.
    """
    def get_something(self, html, *args, **kwargs):
        """An example method, takes argument and return parsed data.
        """
        data = dict()
        return data
    

class UrlEncoder(object):
    """Base Url Encoder. Provide functional interface to create url.
    """
    def something_url(self, *args, **kwargs):
        """An example method, takes argument and return url.
        """
        url = "https://github.com/"
        return url