#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fake_useragent

ua = fake_useragent.UserAgent()


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
