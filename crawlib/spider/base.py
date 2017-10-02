#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class BaseSpider(object):
    default_headers = None
    default_timeout = None
    default_wait_time = 0.0

    def prepare_headers(self, headers):
        if headers is None:
            return self.default_headers
        else:
            return headers

    def prepare_timeout(self, timeout):
        if timeout is None:
            return self.default_timeout
        else:
            return timeout

    def prepare_wait_time(self, wait_time):
        if wait_time is None:
            wait_time = self.default_wait_time
        if wait_time:
            time.sleep(wait_time)
        return wait_time

    def get_html(self, url, *args, **kwargs):
        raise NotImplementedError

    def download(self, url, *args, **kwargs):
        raise NotImplementedError

