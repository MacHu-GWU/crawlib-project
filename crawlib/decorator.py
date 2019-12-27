# -*- coding: utf-8 -*-

"""
There are three major popular libraries widely used for making
http request:

- ``requests``: http://docs.python-requests.org/en/master/
- ``scrapy``: https://doc.scrapy.org/en/latest/topics/request-response.html
- ``selenium``: http://selenium-python.readthedocs.io/index.html

And there are two major popular library widely used for extracting data
from html:

- ``beautifulsoup4``: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- ``scrapy.selector``: https://doc.scrapy.org/en/latest/topics/selectors.html
- ``requests_html``: https://github.com/kennethreitz/requests-html

This module bridge the gap.
"""

import inspect
from six import PY2, PY3

if PY2:
    getfullargspec = inspect.getargspec
elif PY3:
    getfullargspec = inspect.getfullargspec

try:
    from bs4 import BeautifulSoup
except ImportError:
    pass

try:
    from requests_html import HTML
except ImportError:
    pass


class FakeResponse: pass


try:
    from requests import Response as RequestsResponse
except ImportError:  # pragma: no cover
    RequestsResponse = FakeResponse

try:
    from scrapy.http import Response as ScrapyResponse
except ImportError:  # pragma: no cover
    ScrapyResponse = FakeResponse

from .decode import decoder
from .exc import DecodeError, SoupError


def soupify(html):
    """
    Convert html to ``bs4.BeautifulSoup``. It solves api change in bs4.3.
    """
    try:
        return BeautifulSoup(html, "html.parser")
    except Exception as e:  # pragma: no cover
        raise SoupError(str(e))


def convert_rhtml(html):
    """
    Convert html to ``requests_html.HTML``.
    """
    try:
        return HTML(html=html)
    except Exception as e:  # pragma: no cover
        raise SoupError(str(e))


def access_binary(response):
    if isinstance(response, RequestsResponse):
        binary = response.content
    elif isinstance(response, ScrapyResponse):
        binary = response.body
    else:  # pragma: no cover
        raise TypeError("It only support ScrapyResponse or RequestsResponse!")
    return binary


def get_func_fullname(func):
    return func.__module__ + "." + func.__name__


def validate_func_def(func,
                      response_arg="response",
                      html_arg="html",
                      soup_arg="soup",
                      rhtml_arg="rhtml"):
    """
    Validate that :func:`auto_decode_and_soupify` is applicable to this
    function. If not applicable, a ``NotImplmentedError`` will be raised.
    """
    arg_spec = getfullargspec(func)
    if arg_spec.defaults:
        args_with_defaults_mapper = dict(zip(arg_spec.args[-len(arg_spec.defaults):], arg_spec.defaults))
    else:
        args_with_defaults_mapper = dict()
    for arg in [response_arg, html_arg]:
        if arg not in arg_spec.args:
            raise NotImplementedError(
                ("`{func}` has to take the keyword syntax input, example: "
                 "{func}({response_arg}=None, {html_arg}=None, ..., **kwargs)").format(
                    func=get_func_fullname(func),
                    response_arg=response_arg,
                    html_arg=html_arg,
                )
            )
        else:
            if args_with_defaults_mapper.get(arg) is not None:
                raise NotImplementedError(
                    "`{func}` default value for arg `{arg}` has to be None!".format(
                        func=get_func_fullname(func),
                        arg=arg,
                    )
                )

    if ((soup_arg in arg_spec.args) + (rhtml_arg in arg_spec.args)) > 1:
        raise NotImplementedError(
            ("`{func}` can only at none or only one of "
             "`{soup_arg}`, `{rhtml_arg}` arguments!").format(
                func=get_func_fullname(func),
                soup_arg=soup_arg,
                rhtml_arg=rhtml_arg,
            )
        )


validate_func_def_cached = dict()


def resolve_arg(response_arg="response",
                html_arg="html",
                soup_arg="soup",
                rhtml_arg="rhtml",
                encoding="utf-8",
                encoding_error_handler=decoder.ErrorsHandle.ignore):
    """
    This decorator assume that there are at least two arguments ``response`` and
    ``html``, and may have ``soup`` or ``rhtml`` in keyword syntax:

    - ``response``: ``requests.Response`` or ``scrapy.http.Reponse``
    - ``html``: html string
    - ``soup`` for ``bs4.BeautifulSoup`` or ``rhtml`` for ``requests_html.HTML``.

    1. if ``html`` is not available, it will automatically be generated from
        ``response``.
    2. if ``soup`` is not available, it will automatically be generated from
        ``html``.
    3. if ``rhtml`` is not available, it will automatically be generated from
        ``html``.

    Usage::

        @resolve_arg()
        def parse(response=None, html=None, soup=None):
            ...

    **中文文档**

    此装饰器可以免去写类似于如下 code 的麻烦::

        response = requests.get(url)
        html = response.content.decode("utf-8")
        soup = bs4.BeautifulSoup(html, "html.parser")
        # do something ...

    此装饰器会自动检测函数中名为 ``response``, ``html``, ``soup`` 或 ``rhtml`` 参数,
    并在依据: 如果 ``html`` 没有给出, 则去 ``response`` 里找. 如果 ``soup`` 或 ``rhtml``
    没有给出, 则从 ``html`` 中提取.

    被此装饰器装饰的函数必须要有以上提到的三个参数. 并且在使用时, 必须使用keyword的形式进行输入.

    :param request_arg:
    :param response_arg:
    :param html_arg:
    :param soup_arg:
    :param rhtml_arg:
    :param encoding:
    :param encoding_error_handler:
    :return:
    """

    def deco(func):
        func_hash = hash(func)
        if func_hash not in validate_func_def_cached:
            validate_func_def(
                func,
                response_arg=response_arg,
                html_arg=html_arg,
                soup_arg=soup_arg,
                rhtml_arg=rhtml_arg,
            )
            validate_func_def_cached[func_hash] = True

        def wrapper(*args, **kwargs):
            response = kwargs.get(response_arg)
            html = kwargs.get(html_arg)
            soup = kwargs.get(soup_arg)
            rhtml = kwargs.get(rhtml_arg)

            if html is None:
                binary = access_binary(response)
                try:
                    html = decoder.decode(
                        binary=binary,
                        url=response.url,
                        encoding=encoding,
                        errors=encoding_error_handler,
                    )
                except Exception as e:  # pragma: no cover
                    raise DecodeError(str(e))
                kwargs[html_arg] = html

            if soup is None:
                soup = soupify(html)
                kwargs[soup_arg] = soup

            if rhtml is None:
                rhtml = convert_rhtml(html)
                kwargs[rhtml_arg] = rhtml

            return func(*args, **kwargs)

        return wrapper

    return deco
