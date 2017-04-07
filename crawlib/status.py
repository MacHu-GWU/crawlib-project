#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .pkg.constant import Constant
except:
    from crawlib.pkg.constant import Constant


class Status(Constant):

    class S0_ToDo(Constant):
        id = 0
        description = "刚获得Primary Key, 还未尝试过抓取"

    class S1_UrlError(Constant):
        id = 1
        description = "生成Url的过程出现了错误"

    class S2_HttpError(Constant):
        id = 2
        description = "执行spider.get_html(url)失败, 可能是超时, 也可能是Url错误"

    class S3_WrongPage(Constant):
        id = 3
        description = "成功获得了Html, 但Html不是我们想要的, 可能是url出错, 也可能服务器返回了错误页面"

    class S4_ParseError(Constant):
        id = 4
        description = "从Html提取数据时出现异常, 导致无法提取数据下去"

    class S5_InCompleteData(Constant):
        id = 5
        description = "成功提取了数据, 虽然没有出现异常, 但是某些数据点出现了错误, 结果可能不完整"

    class S8_Finished(Constant):
        id = 8
        description = "成功的抓取了所有数据"

    class S9_Finalized(Constant):
        id = 9
        description = "人工对其进行过编辑, 最终确定了, 不会再进行任何的修改"
