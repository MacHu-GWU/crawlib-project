# -*- coding: utf-8 -*-

"""
url builder related utility methods.
"""

from six import PY2
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


def get_domain(url, ensure_http=True):
    """
    Get domain part of an url.

    For example: https://www.python.org/doc/ -> https://www.python.org
    """
    if ensure_http:
        if not (url.startswith("https") or url.startswith("http")):
            raise ValueError("%s not start with `http` or `https`!" % url)

    parse_result = urlparse(url)
    domain = "{schema}://{netloc}".format(
        schema=parse_result.scheme, netloc=parse_result.netloc)
    return domain


def join_all(domain, *parts):
    """
    Join all url components.

    :rtype: str
    :param domain: Domain parts, example: https://www.python.org

    :rtype: list
    :param parts: Other parts, example: "/doc", "/py27"

    :rtype: str
    :return: url

    Example::

        >>> join_all("https://www.apple.com", "iphone")
        https://www.apple.com/iphone
    """
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

    :type endpoint: str
    :param endpoint:

    :type params: list, tuple, dict
    :param params:

    Example::

        >>> add_params("https://www.google.com/search", {"q": "iphone"})
        https://www.google.com/search?q=iphone
    """
    p = PreparedRequest()
    p.prepare(url=endpoint, params=params)
    if PY2:  # pragma: no cover
        return unicode(p.url)
    else:  # pragma: no cover
        return p.url


def get_all_subclass(klass):
    """
    Get all subclass. Return a set.

    :rtype: set
    :return:
    """
    subclasses = set()
    for subklass in klass.__subclasses__():
        subclasses.add(subklass)
        subclasses.update(get_all_subclass(subklass))
    return subclasses
