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
from six import string_types
from crawlib.logger import SpiderLogger


def prepare_kwargs(kwargs):
    if kwargs is None:
        return dict()
    return kwargs


def execute_one_to_many_job(parent_class=None,
                            get_unfinished_kwargs=None,
                            get_unfinished_limit=None,
                            parser_func=None,
                            parser_func_kwargs=None,
                            build_url_func_kwargs=None,
                            downloader_func=None,
                            downloader_func_kwargs=None,
                            post_process_response_func=None,
                            post_process_response_func_kwargs=None,
                            process_item_func_kwargs=None,
                            logger=None,
                            sleep_time=None):
    """
    A standard one-to-many crawling workflow.

    :param parent_class:
    :param get_unfinished_kwargs:
    :param get_unfinished_limit:
    :param parser_func: html parser function.
    :param parser_func_kwargs: other keyword arguments for ``parser_func``
    :param build_url_func_kwargs: other keyword arguments for
        ``parent_class().build_url(**build_url_func_kwargs)``
    :param downloader_func: a function that taking ``url`` as first arg, make
        http request and return response/html.
    :param downloader_func_kwargs: other keyword arguments for ``downloader_func``
    :param post_process_response_func: a callback function taking response/html
        as first argument. You can put any logic in it. For example, you can
        make it sleep if you detect that you got banned.
    :param post_process_response_func_kwargs: other keyword arguments for
        ``post_process_response_func``
    :param process_item_func_kwargs: other keyword arguments for
        ``ParseResult().process_item(**process_item_func_kwargs)``
    :param logger:
    :param sleep_time: default 0, wait time before making each request.
    """
    # prepare arguments
    get_unfinished_kwargs = prepare_kwargs(get_unfinished_kwargs)
    parser_func_kwargs = prepare_kwargs(parser_func_kwargs)
    build_url_func_kwargs = prepare_kwargs(build_url_func_kwargs)
    downloader_func_kwargs = prepare_kwargs(downloader_func_kwargs)
    post_process_response_func_kwargs = prepare_kwargs(
        post_process_response_func_kwargs)
    process_item_func_kwargs = prepare_kwargs(process_item_func_kwargs)

    if post_process_response_func is None:
        def post_process_response_func(response, **kwargs):
            pass

    if not isinstance(logger, SpiderLogger):
        raise TypeError

    if sleep_time is None:
        sleep_time = 0

    # do the real job
    query_set = parent_class.get_all_unfinished(**get_unfinished_kwargs)
    if get_unfinished_limit is not None:
        query_set = query_set.limit(get_unfinished_limit)
    todo = list(query_set)
    logger.log_todo_volumn(todo)

    for parent_instance in todo:
        url = parent_instance.build_url(**build_url_func_kwargs)
        logger.log_to_crawl_url(url)

        logger.log_sleeper(sleep_time)
        time.sleep(sleep_time)

        try:
            response_or_html = downloader_func(url, **downloader_func_kwargs)
            if isinstance(response_or_html, string_types):
                parser_func_kwargs["html"] = response_or_html
            else:
                parser_func_kwargs["response"] = response_or_html
            post_process_response_func(
                response_or_html, **post_process_response_func_kwargs)
        except Exception as e:
            logger.log_error(e)
            continue

        try:
            parse_result = parser_func(
                parent=parent_instance,
                **parser_func_kwargs
            )
            parse_result.process_item(**process_item_func_kwargs)
            logger.log_status(parse_result)
        except Exception as e:
            logger.log_error(e)
            continue
