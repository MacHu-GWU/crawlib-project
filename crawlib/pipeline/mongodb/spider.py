#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
integrate these modules:

- ``crawlib.pipeline.mongodb.orm``
- ``crawlib.data_class``
- ``crawlib.html_parser``
- ``crawlib.logger``
"""

import time


def execute_one_to_many_job(parent_class=None,
                            unfinished_filters=None,
                            limit=None,
                            parser_func=None,
                            parser_func_kwargs=None,
                            downloader=None,
                            downloader_kwargs=None,
                            logger=None,
                            sleep_time=None):
    """
    :param parent_class:
    :param unfinished_filters:
    :param limit:
    :param parser_func:
    :param parser_func_kwargs: other params consumed by html parser function.
    :param downloader:
    :param downloader_kwargs:
    :param logger:
    :param sleep_time:
    :return:
    """
    query_set = parent_class.get_all_unfinished(filters=unfinished_filters)
    if limit is not None:
        query_set = query_set.limit(limit)
    todo = list(query_set)
    logger.log_todo_volumn(todo)

    if parser_func_kwargs is None:
        parser_func_kwargs = dict()
    if downloader_kwargs is None:
        downloader_kwargs = dict()

    for parent_instance in todo:
        url = parent_instance.build_url()
        logger.log_to_crawl_url(url)

        logger.log_sleeper(sleep_time)
        time.sleep(sleep_time)

        try:
            response = downloader.get(url, **downloader_kwargs)
        except Exception as e:
            logger.log_error(e)
            continue

        try:
            parse_result = parser_func(
                response=response,
                parent=parent_instance,
                **parser_func_kwargs
            )
            parse_result.process_item()
            logger.log_status(parse_result)
        except Exception as e:
            logger.log_error(e)
            continue
