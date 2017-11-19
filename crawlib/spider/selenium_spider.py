#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

try:
    from .base import BaseSpider
except:  # pragma: no cover
    from crawlib.spider.base import BaseSpider


class BaseSeleniumSpider(BaseSpider):
    """

    """

    def __init__(self,
                 driver=None,
                 default_timeout=None,
                 default_headers=None,
                 default_wait_time=0.0):
        self.driver = driver
        self.default_headers = default_headers
        self.default_timeout = default_timeout
        self.default_wait_time = default_wait_time
        self.domain_encoding_table = dict()

    def get_html(self, url, wait_time=None):
        """
        Get html source in text.
        """
        wait_time = self.prepare_wait_time(wait_time)
        if wait_time:
            self.sleep(wait_time)

        self.driver.get(url)
        return self.driver.page_source

    def close(self):
        self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


class ChromeSpider(BaseSeleniumSpider):  # pragma: no cover
    """
    Chrome Browser Simulator.
    """

    def __init__(self, driver_executable_path,
                 default_timeout=None,
                 default_headers=None,
                 default_wait_time=0.0):
        driver = webdriver.Chrome(executable_path=driver_executable_path)
        super(ChromeSpider, self).__init__(
            driver=driver,
            default_timeout=default_timeout,
            default_headers=default_headers,
            default_wait_time=default_wait_time,
        )


if __name__ == "__main__":
    path = "/Users/sanhehu/Documents/chromedriver"
    spider = ChromeSpider(path)
    with spider as spider:
        html = spider.get_html("https://www.python.org/")
        spider.sleep(10)
