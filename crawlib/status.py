# -*- coding: utf-8 -*-

"""
Http requests and Html parse status code table.
"""

from constant2 import Constant


class StatusDetail(Constant):
    """
    Status Class Template.
    """
    id = None
    description = None
    description_en = None
    description_cn = None


class Status(Constant):
    """
    Crawler Status Code Map.
    """

    class S0_ToDo(StatusDetail):
        id = 0
        description = "To do"
        description_en = description
        description_cn = "还未对以该Primary Key为基准生成的Url尝试过抓取。"

    class S5_UrlError(StatusDetail):
        id = 5
        description = "Failed to build url endpoint"
        description_en = description
        description_cn = "生成Url的过程出现了错误。"

    class S10_HttpError(StatusDetail):
        id = 10
        description = "Failed to make a http request."
        description_en = description
        description_cn = "执行spider.get_html(url)失败，无法获得响应。"

    class S20_WrongPage(StatusDetail):
        id = 20
        description = ("Successfully get http request, but get the wrong html"
                       "could be due to Banned, server temporarily not available.")
        description_en = description
        description_cn = ("成功获得了Html, 但Html不是我们想要的，"
                          "可能是由于被Ban, 服务器临时出错等情况，"
                          "使得服务器返回了错误的页面。")

    class S25_DecodeError(StatusDetail):
        id = 25
        description = ("Failed to decode binary response.")
        description_en = description
        description_cn = ("无法从http响应的字节码中解码出字符串。")

    class S30_ParseError(StatusDetail):
        id = 30
        description = "Html parser method failed."
        description_en = description
        description_cn = "在从Html提取数据时出现异常，导致程序失败。"

    class S40_InCompleteData(StatusDetail):
        id = 40
        description = "Html parser method success, but data is wrong."
        description_en = description
        description_cn = ("提取数据的函数被成功运行，虽然没有出现异常，"
                          "但是某些数据点出现了错误, 结果可能不完整。")

    class S50_Finished(StatusDetail):
        """
        Break point, status code greater than this should be consider as 'Finished'.
        """
        id = 50
        description = "Finished."
        description_en = description
        description_cn = "成功的抓取了所有数据"

    class S60_ServerSideError(StatusDetail):
        id = 60
        description = "Serverside error, so we temporarily mark it as 'finished'."
        description_en = description
        description_cn = ("服务器端出现问题，导致该Url是不可能被抓取的，"
                          "或是目前的数据不是我们最终想要的，但是可以凑活暂时用，"
                          "我们暂时将其标记为完成，但以后可能再次进行尝试。")

    class S99_Finalized(StatusDetail):
        id = 99
        description = "Finalized, will nolonger be crawled / changed."
        description_en = description
        description_cn = "强制禁止对其进行任何的修改和抓取，通常是由于有人工修改介入。"


FINISHED_STATUS_CODE = Status.S50_Finished.id
