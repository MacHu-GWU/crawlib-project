#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import fake_useragent
import timeout_decorator


# fake useragent grabs data from useragentstring.com, and it may fail.
@timeout_decorator.timeout(3)
def get_ua():
    return fake_useragent.UserAgent()

try:
    ua = get_ua()
    ua_all = [
        ua.ie,
        ua.msie,
        ua['Internet Explorer'],
        ua.opera,
        ua.chrome,
        ua.google,
        ua['google chrome'],
        ua.firefox,
        ua.ff,
        ua.safari,
    ]
except: # manually build fake user agent
    class UserAgentCollection(object):
        ie = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)"
        firefox = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)"
        ff = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
        chrome = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        google = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15"
        msie = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
        opera = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991"

        _all = [
            ie, firefox, ff, chrome, google, safari, msie, opera,
        ]

        @property
        def random(self):
            return random.choice(self._all)


    ua = UserAgentCollection()
    ua_all = ua._all


class Headers(object):
    """
    Frequent used request header.
    """

    class UserAgent(object):
        KEY = "User-Agent"

        ie = ua.ie
        chrome = ua.chrome
        firefox = ua.firefox
        safari = ua.safari

        _all = ua_all

        @classmethod
        def random_by_statistic(cls):
            return ua.random

        @classmethod
        def random(cls):
            return random.choice(cls._all)

    class ContentType(object):
        KEY = "Content-Type"

        html_utf8 = "text/html; charset=utf-8"
        json_utf8 = "application/json; charset=utf-8"

    class Connection(object):
        KEY = "Connection"

        keep_alive = "keep-alive"
        close = "close"

    class Accept(object):
        KEY = "Accept"

        html = "text/html"
        json = "application/json"
        xml = "application/xml"
        image = "image/*"

    class AcceptLanguage(object):
        KEY = "Accept-Language"

        en_US = "en-US,en"
        zh_CN = "zh-CN,zh"

        class Languages(object):
            en_US = "en-US,en"
            zh_CN = "zh-CN,zh"
            zh_TW = "zh-TW,zh"

    class Referer(object):
        KEY = "Referer"
