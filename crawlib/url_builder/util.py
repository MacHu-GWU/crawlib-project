#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests.compat import urlparse
from requests.models import PreparedRequest


def get_netloc(url):
    """
    Get network location part of an url.

    For example: https://www.python.org/doc/ -> www.python.org
    """
    parse_result = urlparse(url)
    netloc = parse_result.netloc
    return netloc


def get_domain(url):
    """
    Get domain part of an url.

    For example: https://www.python.org/doc/ -> https://www.python.org

    :param url:
    :return:
    """
    parse_result = urlparse(url)
    domain = "{schema}://{netloc}".format(
        schema=parse_result.scheme, netloc=parse_result.netloc)
    return domain


def join_all(domain, *parts):
    """
    Join all url components.

    :param domain: Domain parts, example: https://www.python.org
    :param parts: Other parts, example: "/doc", "/py27"
    :return: url
    """
    if " " in ([domain, ] + list(parts)):
        raise Exception("empty string is not allowed in url!")

    l = list()

    if domain.endswith("/"):
        domain = domain[:-1]
    l.append(domain)

    for part in parts:
        for i in part.split("/"):
            if i.strip():
                l.append(i)
    url = "/".join(l)
    return url


def add_params(endpoint, params):
    """
    Combine query endpoint and params.
    """
    p = PreparedRequest()
    p.prepare(url=endpoint, params=params)
    return p.url