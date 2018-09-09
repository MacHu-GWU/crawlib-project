#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loggerFactory.logger import BaseLogger


class SpiderLogger(object):  # pragma: no cover
    """
    Integrate the spider with the logging system. Includes some frequently
    used log command.
    """

    def __init__(self, logger):
        if not isinstance(logger, BaseLogger):
            raise TypeError

        self.logger = logger

        self._n_todo = None
        self._nth_counter = None

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

    def show(self, *args, **kwargs):
        self.logger.show(*args, **kwargs)

    __call__ = show

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

    def log_parsed_result(self, parse_result, child_limit=3):
        item = parse_result
        self.logger.info(str(item["parent"]), 1)
        for i in range(1, item._settings_NUMBER_OF_CHILD_TYPES_required + 1):
            for child in item.get_child_list(i)[:child_limit]:
                self.logger.info(str(child), 1)
