#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SpiderLogger(object):  # pragma: no cover
    """
    Integrate the spider with the logging system. Includes some frequently
    used log command.
    """

    def __init__(self, logger):
        self.logger = logger

        self._n_todo = None
        self._nth_counter = None

    def log_todo_volumn(self, obj_list):
        self.logger.info("Job Start!")

        _n_todo = len(obj_list)
        self._n_todo = _n_todo
        self._nth_left_counter = _n_todo
        msg = "There are {} items in our todo list.".format(_n_todo)
        self.logger.info(msg)

    def log_to_crawl_url(self, url):
        self._nth_left_counter -= 1
        msg = "Crawling {}, {} left ...".format(url, self._nth_left_counter)
        self.logger.info(msg)

    def log_sleeper(self, sleep_time):
        msg = "sleep for {} seconds ...".format(sleep_time)
        self.logger.info(msg, 1)

    def log_status(self, parse_result):
        msg = "status: {}, log: {}".format(
            parse_result.status, parse_result.log)
        self.logger.info(msg, 1)

    def log_error(self, e):
        self.logger.info(str(e), 1)
