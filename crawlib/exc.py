# -*- coding: utf-8 -*-

"""
Exceptions.
"""

from .status import Status


# HtmlParser error
class CaptchaError(Exception):
    """
    Encounter a captcha page.

    http status code 403

    **中文文档**

    遭遇反爬虫验证页面。
    """
    status_code = Status.S20_WrongPage.id


class ForbiddenError(Exception):
    """
    Banned from server.

    http status code 403

    **中文文档**

    被服务器禁止访问。
    """
    status_code = Status.S20_WrongPage.id


class WrongHtmlError(Exception):
    """
    The html is not the one we desired.

    **中文文档**

    页面不是我们想要的页面。有以下几种可能:

    1. 服务器暂时连不上, 返回了404页面。
    2. 服务器要求验证码, 返回了验证码页面。
    3. 页面暂时因为各种奇怪的原因不是我们需要的页面。
    """
    status_code = Status.S20_WrongPage.id


class DecodeError(Exception):
    """
    Failed to decode binary response.
    """
    status_code = Status.S25_DecodeError.id


class SoupError(Exception):
    """
    Failed to convert html to beatifulsoup.

    http status 200+

    **中文文档**

    html成功获得了, 但是格式有错误, 不能转化为soup。
    """
    status_code = Status.S30_ParseError.id


class ParseError(Exception):
    """
    Failed to parse data from html, may due to bug in your method.

    **中文文档**

    由于函数的设计失误, 解析页面信息发生了错误。
    """
    code = Status.S30_ParseError.id


class IncompleteDataError(Exception):
    """
    Successfully parse data from html, but we can't accept the result due to
    missing data.
    """
    status_code = Status.S40_InCompleteData.id


class ServerSideError(Exception):
    """
    Server side problem.

    code 404

    **中文文档**

    1. 因为服务器的缘故该页面无法正常访问, 也可能已经不存在了, 但以后可能会回来。
    2. 因为服务器的缘故, 上面的数据不是我们想要的, 但是我们可以暂时用着, 以后可能要重新抓取。
    """
    status_code = Status.S60_ServerSideError.id


# Other errors
class DownloadOversizeError(Exception):
    """
    The download target are not falls in the size range you specified.
    """
