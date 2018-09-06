#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

``Extended``

每当我们收到一个 ``Request`` 之后, ``DownloaderMiddleWare`` 会给我们传回一个
``Response``. 而我们会用在 ``HtmlParser`` 中定义的以 ``parse`` 开头的方法来对
``Response`` 中的html进行解析. 在这个解析过程中, 解析的结果会被放入
:class:`ParseResult` 类中. 这个类除了包含了:

- 解析中被传输的参数.
- 经过解析, 判断解析是否成功了. 如果不成功, 判断是解析中出了差错, 还是这个 ``Response``
    本身就是错误的. 然后保存状态码.
- 记录该次解析开始的时间.

还包含一个重要的属性 :attr:`ParseResult.item``. 这个item是一个 :class:`Scrapy.Item`
的子类. 包含了我们所感兴趣的数据本体.
"""

import attr
from datetime import datetime

try:
    from scrapy import Item, Field
except:  # pragma: no cover
    from ._scrapy_item import Item, Field
try:
    from .status import Status
except:  # pragma: no cover
    from crawlib.status import Status


class ExtendedItem(Item):
    """
    An abstract data container class hold data that is extracted from html.
    """
    _settings_MONGOENGZINE_CLASS_optional = None
    _settings_SQLALCHEMY_ORM_CLASS_optional = None

    def to_me_orm(self):
        """
        take data out, and put in corresponding mongoengine orm class.
        """
        return self._settings_MONGOENGZINE_CLASS_optional(**dict(self))

    def to_sa_orm(self):
        """
        take data out, and put in corresponding sqlalchemy orm class.
        """
        return self._settings_SQLALCHEMY_ORM_CLASS_optional(**dict(self))

    def process(self, parse_result, **kwargs):
        """
        define a method that how this method been processed
        """
        raise NotImplementedError


class OneToManyItem(ExtendedItem):
    """
    One To

    :param parent_class: a :class:`mongoengine.Document` class.
    :param parent: instance of :class:`mongoengine.Document`.

    **中文文档**

    """
    _settings_NUMBER_OF_CHILD_TYPES_required = None
    _settings_N_CHILD_1_KEY_optional = None
    _settings_N_CHILD_2_KEY_optional = None
    _settings_N_CHILD_3_KEY_optional = None
    _settings_N_CHILD_4_KEY_optional = None
    _settings_N_CHILD_5_KEY_optional = None

    parent_class = Field()
    parent = Field()

    child_class_1 = Field()
    child_class_2 = Field()
    child_class_3 = Field()
    child_class_4 = Field()
    child_class_5 = Field()

    child_list_1 = Field()
    child_list_2 = Field()
    child_list_3 = Field()
    child_list_4 = Field()
    child_list_5 = Field()

    _max_number_of_child_types = 5
    """
    Don't change this class variable!
    """

    def __init__(self, *args, **kwargs):
        super(OneToManyItem, self).__init__(*args, **kwargs)
        self.post_init()

    @classmethod
    def validate_implementation(cls):
        if cls._settings_NUMBER_OF_CHILD_TYPES_required not in range(cls._max_number_of_child_types + 1):
            msg = ("`_settings_NUMBER_OF_CHILD_TYPES_required` has to be "
                   "equal to or less than `_max_number_of_child_types`!")
            raise ValueError(msg)

    def post_init(self):
        for nth in range(1, self._settings_NUMBER_OF_CHILD_TYPES_required + 1):
            self["child_list_%s" % nth] = list()

    def get_n_child(self, nth=1):
        return len(self["child_list_%s" % nth])

    def get_child_class(self, nth=1):
        return self["child_class_%s" % nth]

    def get_child_list(self, nth=1):
        return self["child_list_%s" % nth]

    def append_child(self, child, nth=1):
        self["child_list_%s" % nth].append(child)


class OneToManyMongoEngineItem(OneToManyItem):  # pragma: no cover
    def process(self, parse_result, **kwargs):
        if parse_result.is_finished():
            parent = self["parent"]
            if not (parent is None):
                # update `n_child` field
                for nth in range(1, 1 + self._settings_NUMBER_OF_CHILD_TYPES_required):
                    n_child_key = getattr(
                        self, "_settings_N_CHILD_%s_KEY_optional" % nth)
                    if n_child_key is not None:
                        setattr(
                            parent,
                            n_child_key,
                            self.get_n_child(nth),
                        )

            # smart insert children
            for nth in range(1, 1 + self._settings_NUMBER_OF_CHILD_TYPES_required):
                child_class = self.get_child_class(nth)
                if not (child_class is None):
                    child_class.smart_insert(self.get_child_list(nth))

            # update parent
            if not (parent is None):
                setattr(parent, parent._settings_STATUS_KEY_required,
                        parse_result.status)
                setattr(parent, parent._settings_EDIT_AT_KEY_required,
                        parse_result.create_at)
                parent.smart_update(parent)


class OneToManyRdsItem(OneToManyItem):  # pragma: no cover
    def process(self, parse_result, engine, **kwargs):
        if parse_result.is_finished():
            parent = self["parent"]
            if not (parent is None):
                # update `n_child` field
                for nth in range(1, 1 + self._settings_NUMBER_OF_CHILD_TYPES_required):
                    n_child_key = getattr(
                        self, "_settings_N_CHILD_%s_KEY_optional" % nth)
                    if n_child_key is not None:
                        setattr(
                            parent,
                            n_child_key,
                            self.get_n_child(nth),
                        )

            # smart insert children
            for nth in range(1, 1 + self._settings_NUMBER_OF_CHILD_TYPES_required):
                child_class = self.get_child_class(nth)
                if not (child_class is None):
                    child_class.smart_insert(engine, self.get_child_list(nth))

            # update parent
            if not (parent is None):
                setattr(
                    parent,
                    parent._settings_STATUS_KEY_required,
                    parse_result.status,
                )
                setattr(
                    parent,
                    parent._settings_EDIT_AT_KEY_required,
                    parse_result.create_at,
                )
                parent.update_all(engine, parent)


@attr.s
class ParseResult(object):
    """
    A data container class holds:

    - extracted item
    - request and response info
    - status info
    - time info

    :param params: parser function parameters. parser函数的所有参数.
    :param item: parsed data. 从html中解析出的数据.
    :param log: error dictionary.
    :param status: int, status code. 抓取状态码.
    :param time: datetime. 抓取的时间.
    """
    params = attr.ib(default=attr.Factory(dict))
    item = attr.ib(
        default=None,
        validator=attr.validators.optional(
            attr.validators.instance_of(ExtendedItem)
        )
    )
    log = attr.ib(default=attr.Factory(dict))
    status = attr.ib(default=None)
    create_at = attr.ib(default=attr.Factory(datetime.now))

    _param_key = "params"
    _item_key = "item"
    _log_key = "log"
    _status_key = "status"
    _create_at_key = "create_at"

    _settings_FINISHED_STATUS_CODE_required = Status.S50_Finished.id

    def to_dict(self):  # pragma: no cover
        return attr.asdict(self)

    def set_status_todo(self):
        self.status = Status.S0_ToDo.id

    def set_status_url_error(self):
        self.status = Status.S5_UrlError.id

    def set_status_http_error(self):
        self.status = Status.S10_HttpError.id

    def set_status_wrong_page(self):
        self.status = Status.S20_WrongPage.id

    def set_status_decode_error(self):
        self.status = Status.S25_DecodeError.id

    def set_status_parse_error(self):
        self.status = Status.S30_ParseError.id

    def set_status_incomplete_data(self):
        self.status = Status.S40_InCompleteData.id

    def set_status_finished(self):
        self.status = self._settings_FINISHED_STATUS_CODE_required

    def set_status_server_side_error(self):
        self.status = Status.S60_ServerSideError.id

    def set_status_finalized(self):
        self.status = Status.S99_Finalized.id

    def is_finished(self):
        """
        test if the status should be marked as `finished`.
        """
        try:
            return self.status >= self._settings_FINISHED_STATUS_CODE_required
        except:  # pragma: no cover
            return False

    def process_item(self, **kwargs):
        """
        Could be used for item pipeline in scrapy framework.
        """
        self.item.process(parse_result=self, **kwargs)
