# -*- coding: utf-8 -*-

import random
import string
from abc import abstractmethod
from datetime import datetime
from typing import List, Dict, Set, Optional, Type, Union, Iterable

import attr
import six
from loggerFactory import StreamOnlyLogger

from ..status import Status, FINISHED_STATUS_CODE
from ..util import get_all_subclass


class EntityBase(object):
    logger = StreamOnlyLogger(name="".join(random.sample(string.hexdigits, 16)))

    @classmethod
    def full_classname(cls):
        return cls.__module__ + "." + cls.__name__

    @abstractmethod
    def build_url(self, **kwargs):
        """
        Build ``url`` endpoint based on the current ORM Entity object.

        .. note::

            User has to implement this method!

        :rtype: str
        """
        msg = ("implement `Entity.build_url(**kwargs)` method yourself, "
               "it build the url endpoint based on the current ORM entity object.")
        raise NotImplementedError(msg)

    def _build_url(self, **kwargs):
        """
        :rtype: str
        """
        return self.build_url(**kwargs)

    @abstractmethod
    def build_request(self, url, **kwargs):
        """
        Build http ``Request`` object from url. You can choose any http library
        you want to use. For example: ``requests`` or ``aiohttp``.

        .. note::
        
            User has to implement this method!
        """
        msg = ("implement `Entity.build_request(url, **kwargs)` method yourself, "
               "it build a http Request object from url, "
               "you can choose any http library, such as `requests` or ``aiohttp`")
        raise NotImplementedError(msg)

    def _build_request(self, url, **kwargs):
        url = self._build_request(url, **kwargs)
        indent = 1
        msg = "|%s| crawling %s ..." % (indent, url)
        self.logger.info(msg, indent)
        return url

    @abstractmethod
    def send_request(self, request, **kwargs):
        """
        Send the http ``Request`` object and returns a ``Response`` object.
        You can choose any http library you want to use.
        For example: ``requests`` or ``aiohttp``.

        .. note::

            User has to implement this method!
        """
        msg = ("implement `Entity.send_request(request, **kwargs)` method yourself, "
               "it send the http Request object and get a Response object, "
               "you can choose any http library, such as `requests` or ``aiohttp`")
        raise NotImplementedError(msg)

    def _send_request(self, request, **kwargs):
        return self.send_request(request, **kwargs)

    @abstractmethod
    def parse_response(self, url, request, response, **kwargs) -> 'ParseResult':
        """
        Extract data from ``Response`` object

        :param url:
        :param request:
        :param response:
        :param kwargs:
        :return:

        .. note::

            User has to implement this method!

        **中文文档**

        爬虫的关键步骤, 解析 http Response 对象, 返回一个 :class:`ParseResult` 对象,
        该对象包含了 url 对应的页面上, 跟当前 Entity 直接相关的信息; 其他的 Entity 的
        信息; 解析过程中出现的错误; 整个解析过程的状态码.

        此函数要求无论中间出现什么样的错误, 都要能够成功返回一个 :class:`ParseResult` 对象.

        根据你使用的 http 库自行编写该函数.
        """
        msg = ("implement `Entity.send_request(request, **kwargs)` method yourself, "
               "it send the http Request object and get a Response object, "
               "you can choose any http library, such as `requests` or ``aiohttp`")
        raise NotImplementedError(msg)

    @abstractmethod
    def process_pr(self, pres: 'ParseResult', **kwargs):
        """
        Process Parse Result.

        :type pres: ParseResult
        :param pres:

        :return:
        """
        raise NotImplementedError


class EntityExtendScheduler(EntityBase):
    """

    **中文文档**

    :parram CONF_STATUS_KEY:
    :parram CONF_EDIT_AT_KEY:
    :parram CONF_FINISHED_STATUS:
    :parram CONF_UPDATE_INTERVAL:
    :parram CONF_UPDATE_FIELDS: 如果不为 None, 则在更新此 Entity 时, 只更新部分的值,
        其中 ``CONF_STATUS_KEY``, ``CONF_EDIT_AT_KEY`` 永远被更新.
    :parram CONF_ONLY_FIELDS:
    """
    CONF_STATUS_KEY = None  # type: str # usually it is "status"
    CONF_EDIT_AT_KEY = None  # usually it is "edit_at"
    CONF_FINISHED_STATUS = FINISHED_STATUS_CODE  # Default 50
    CONF_UPDATE_INTERVAL = 365 * 24 * 60 * 60  # Default 1 Day

    CONF_UPDATE_FIELDS = None # type: tuple
    CONF_ONLY_FIELDS = None # type: tuple
    CONF_RELATIONSHIP = None  # type: RelationshipConfig

    @classmethod
    @abstractmethod
    def get_unfinished(cls, **kwargs) -> Iterable[Union[EntityBase, 'EntityExtendScheduler', 'Entity']]:
        """
        Execute a query to get all **Not Finished** web page ORM entity
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def count_unfinished(cls, **kwargs) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_finished(cls, **kwargs) -> Iterable[Union[EntityBase, 'EntityExtendScheduler', 'Entity']]:
        """
        Execute a query to get all **Finished** web page ORM entity
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def count_finished(cls, **kwargs) -> int:
        raise NotImplementedError

    @classmethod
    def get_all_subclass(cls) -> Set['EntityExtendScheduler']:
        return get_all_subclass(cls)

    def filter_update_data(self):
        """
        :rtype: dict

        **中文文档**

        使用 `CONF_UPDATE_FIELDS` 中定义的属性过滤数据, 只保存那些需要被更新的属性.
        """
        entity_data = self.to_dict()
        entity_data_to_update = {
            field: entity_data[field]
            for field in self.CONF_UPDATE_FIELDS
            if field in entity_data
        }
        return entity_data_to_update

    @classmethod
    def validate_implementation_additional(cls):
        """
        Run ORM framework specified implementation validation
        """
        pass

    @classmethod
    def validate_implementation(cls):
        """
        Check if the subclass of :class:`EntityOrm` is correctly implemented.
        """
        if cls.CONF_STATUS_KEY is None:
            raise NotImplementedError("you have to specify `CONF_STATUS_KEY`!")
        if not isinstance(cls.CONF_STATUS_KEY, six.string_types):
            raise TypeError("`CONF_STATUS_KEY` has to be a str!")

        if cls.CONF_EDIT_AT_KEY is None:
            raise NotImplementedError("you have to specify `CONF_EDIT_AT_KEY`!")
        if not isinstance(cls.CONF_EDIT_AT_KEY, six.string_types):
            raise TypeError("`CONF_EDIT_AT_KEY` has to be a str!")

        #
        msg = ("you have to specify `CONF_UPDATE_FIELDS`!"
               "it is the tuple of field name that you want to update "
               "when you crawled the url generated by cls.build_url(**kwargs)")
        if cls.CONF_UPDATE_FIELDS is None:
            raise NotImplementedError(msg)
        elif isinstance(cls.CONF_UPDATE_FIELDS, (tuple, list)):
            for field in cls.CONF_UPDATE_FIELDS:
                if not hasattr(cls, field):
                    msg = ("`CONF_UPDATE_FIELDS` has '{}', but attribute '{}' "
                           "not found in {}").format(
                        field, field, cls
                    )
                    raise NotImplementedError(msg)

            tmp_lst = list(cls.CONF_UPDATE_FIELDS)
            if "_id" not in tmp_lst:
                tmp_lst.append("_id")
            if cls.CONF_STATUS_KEY not in tmp_lst:
                tmp_lst.append(cls.CONF_STATUS_KEY)
            if cls.CONF_EDIT_AT_KEY not in tmp_lst:
                tmp_lst.append(cls.CONF_EDIT_AT_KEY)
            cls.CONF_UPDATE_FIELDS = tuple(tmp_lst)
        else:
            raise ValueError(msg)

        cls.validate_implementation_additional()

    @classmethod
    def validate_relationship_config(cls):
        """
        Validate ``cls.CONF_RELATIONSHIP``

        This method should be only called from ``Entity.validate_relationship_config()``,
        SHOULD NOT called from the subclass of :class:`Entity`.
        """
        subclasses = cls.get_all_subclass()

        for subclass in subclasses:
            if len(subclass.CONF_RELATIONSHIP.mapping) == 0:
                continue

            for klass, relationship in subclass.CONF_RELATIONSHIP.mapping.items():
                # all related klass has to be subclass of Entity
                if klass not in subclasses:
                    msg = "`{}` is not subclass of `crawlib2.Entity`".format(
                        klass.full_classname()
                    )
                    raise NotImplementedError(msg)

                # check if "relationship" value is valid
                if relationship.relationship not in ["one", "many"]:
                    msg = "`relationship` has to be one of 'one' or 'many'!"
                    raise NotImplementedError(msg)

                # if it is many relationship, check n_child_key field
                if relationship.relationship == "many":
                    # forget to define `n_child_key` attribute with
                    # ORM column / field
                    if not hasattr(subclass, relationship.n_child_key):
                        msg = "`{}` doesn't define `{}` attribute!".format(
                            subclass.full_classname(), relationship.n_child_key
                        )
                        raise NotImplementedError(msg)


class Relationship(object):
    """
    :class:`Relationship` defines crawlable entity relationship.

    Use blog app as example. You want to extract all Post from ListPage.
    Then on ListPage should have many Post. So one ListPage has ``MANY`` Post.

    Then you can define the relationship this way::

        Relationship(child_klass=Post, relationship="many", n_child_key="n_post")

    .. note::

        One crawlable entity may relate to multiple child entity.
        See :class:`RelationshipConfig` for more info.

    **中文文档**

    在 crawlib 框架中, 所有的 url 背后都对应着一个 Entity. Relationship 类定义了
    当前的 Entity 与其他的 Entity 类之间的关系.

    一对一关系. 常用于下载页面. 例如包含了一个图片的页面, 第一步我们要访问页面, 获得图片的地址.
    第二部我们要将图片下载到本地. 这时我们可以定义主 Entity 为 Page, 子 Entity 为 Image.
    其中 Image 是 Page 的 Subclass, 直接继承而来, 并且共用一个数据表.

    一对多关系. 常用于当前 url 上的链接对应的新 url 隶属不同的 ORM Entity, 也就是不同
    的数据表 的情况.

    :param child_klass: 在 parent entity class 页面中能抓取到的 child entity klass
        类.
    :param relationship: "one" or "many" 表示是 1 对多或一对 1 的关系.
    :param n_child_key:
    :param recursive: 只有当 recursive 为 True 时, 才会在执行广度优先爬虫时, 爬完一个
        entity 之后, 继续爬下一个 child entity. 设置为 False 时, 则表示仅仅将 child
        entity 存入数据库, 而并不对 child entity 对应的 url 做抓取.
    """

    class Option(object):
        one = "one"
        many = "many"

    def __init__(self,
                 child_klass: Type[EntityBase],
                 relationship: str,
                 n_child_key: str = None,
                 recursive: bool = True):
        if not issubclass(child_klass, EntityBase):
            msg = "'{}' has to be subclass of 'Entity'!".format(child_klass)
            raise TypeError(msg)
        if relationship not in (self.Option.one, self.Option.many):
            msg = "`relationship` has to be one of 'one' or 'many'!"
            raise ValueError(msg)
        if (n_child_key is None) and (relationship == self.Option.many):
            msg = "you have to specify `n_child_key` when `relationship` is 'many'!"
            raise ValueError(msg)
        self.child_klass = child_klass
        self.relationship = relationship
        self.n_child_key = n_child_key
        self.recursive = recursive


class RelationshipConfig(object):
    """
    This class defines crawlable entity class's relationship.

    **中文文档**

    简单来说, 就是一个 Parent Entity 页面上, 可能会出现哪些 Child Entity 的数据.
    """

    def __init__(self, relationship_collection: List[Relationship] = None):
        """
        :type relationship_collection: List[Relationship]
        :param relationship_collection:
        """
        if relationship_collection is None:
            relationship_collection = list()
        self.relationship_collection = relationship_collection  # type: List[Relationship]
        self.mapping = dict()  # type: Dict[Type[EntityExtendScheduler], Relationship]
        for relationship in relationship_collection:
            self.mapping[relationship.child_klass] = relationship

    def get_relationship(self, klass: Type[Union[EntityBase, 'Entity']]) -> str:
        """
        Get relationship of the parent Entity to the child Entity.
        """
        return self.mapping[klass].relationship

    def get_n_child_key(self, klass: Type[Union[EntityBase, 'Entity']]) -> str:
        """
        Get the column / field name that identified how many child it has
        in ORM entity class.
        """
        return self.mapping[klass].n_child_key

    def __iter__(self):
        return iter(self.mapping)

    def iter_recursive_child_class(self) -> Iterable[Union[EntityBase, 'Entity']]:
        """
        A method that yield child entity class to crawl when current entity is done.
        """
        for relationship in self.relationship_collection:
            if relationship.recursive:
                yield relationship.child_klass


EntityExtendScheduler.CONF_RELATIONSHIP = RelationshipConfig()


class Entity(EntityExtendScheduler):
    def start(self,
              build_url_kwargs=None,
              build_request_kwargs=None,
              send_request_kwargs=None,
              parse_response_kwargs=None,
              process_pr_kwargs=None,
              detailed_log=False,
              left_counter=None):
        """

        **VERY IMPORTANT METHOD**:

        :param build_url_kwargs:
        :param build_request_kwargs:
        :param send_request_kwargs:
        :param parse_response_kwargs:
        :param process_pr_kwargs:
        :return:

        **中文文档**

        执行如下流程:

        访问一个 Entity 所对应的 url, 从 HTML 中提取数据后, 将数据保存到数据库,
        更新 Entity 对应的表, 以及其他相关的表. 其中在处理阶段, 可以定义如下载等操作.
        """
        # pre process additional kwargs
        if build_url_kwargs is None:
            build_url_kwargs = dict()
        if build_request_kwargs is None:
            build_request_kwargs = dict()
        if send_request_kwargs is None:
            send_request_kwargs = dict()
        if parse_response_kwargs is None:
            parse_response_kwargs = dict()
        if process_pr_kwargs is None:
            process_pr_kwargs = dict()

        # build url
        try:
            url = self.build_url(**build_url_kwargs)
            indent = 1
            msg = "|%s| crawling %s, %s url left ..." % (indent, url, left_counter)
            self.logger.info(msg, indent)
        except Exception as e:
            pres = ParseResult(
                entity=self,
                data={"errors": str(e)},
                status=Status.S5_UrlError.id
            )
            self.process_pr(pres, **process_pr_kwargs)
            return

        # build request
        try:
            if detailed_log:
                indent = 2
                msg = "|%s| build Request object ..." % indent
                self.logger.info(msg, indent)
            request = self.build_request(url, **build_request_kwargs)
        except Exception as e:
            indent = 2
            msg = "|%s| Failed to build HTTP Request object!" % indent
            self.logger.info(msg, indent)
            pres = ParseResult(
                entity=self,
                data={"errors": str(e)},
                status=Status.S10_HttpError.id
            )
            self.process_pr(pres, **process_pr_kwargs)
            return

        # send request
        try:
            if detailed_log:
                indent = 2
                msg = "|%s| make HTTP request ..." % indent
                self.logger.info(msg, indent)
            response = self.send_request(request, **send_request_kwargs)
        except Exception as e:
            indent = 2
            msg = "|%s| Failed to get HTTP response!" % indent
            self.logger.info(msg, indent)
            pres = ParseResult(
                entity=self,
                data={"errors": str(e)},
                status=Status.S10_HttpError.id
            )
            self.process_pr(pres, **process_pr_kwargs)
            return

        # parse response
        try:
            if detailed_log:
                indent = 2
                msg = "|%s| parse HTTP response ..." % indent
                self.logger.info(msg, indent)
            pres = self.parse_response(
                url=url,
                request=request,
                response=response,
                **parse_response_kwargs,
            )
        except Exception as e:
            indent = 2
            msg = "|%s| Failed to parse http response!" % indent
            self.logger.info(msg, indent)
            pres = ParseResult(
                entity=self,
                data={"errors": str(e)},
                status=Status.S30_ParseError.id
            )
            self.process_pr(pres, **process_pr_kwargs)
            return

        # process parse_result
        try:
            if detailed_log:
                indent = 2
                msg = "|%s| process parse result ..." % indent
                self.logger.info(msg, indent)
            self.process_pr(pres, **process_pr_kwargs)
            if pres.is_finished():
                indent = 2
                msg = "|%s| Success!" % indent
                self.logger.info(msg, indent)
            else:
                indent = 2
                msg = "|%s| %s" % (indent, Status.GetFirst("id", pres.status).description)
                self.logger.info(msg, indent)
        except Exception as e:
            indent = 2
            msg = "|%s| Failed to process parse result!" % indent
            self.logger.info(msg, indent)

    @classmethod
    def start_all(cls,
                  detailed_log=False,
                  **kwargs):
        indent = 0
        n_unfinished = cls.count_unfinished()
        left_counter = n_unfinished
        msg = "|%s| Working on Entity(%s), got %s url to crawl ..." % (indent, cls, n_unfinished)
        cls.logger.info(msg, indent)

        # crawl current unfinished entity
        for entity in list(cls.get_unfinished()):
            # entity.start(detailed_log=detailed_log, left_counter=0)
            left_counter -= 1
            entity.start(detailed_log=detailed_log, left_counter=left_counter)

        # crawl related entity
        for klass in cls.CONF_RELATIONSHIP.iter_recursive_child_class():
            klass.start_all(detailed_log=detailed_log)


@attr.s
class ParseResult(object):
    """
    **中文文档**

    ParseResult 是 crawlib 广度优先框架中所使用的类, 用于包装从 html 抓取的数据.
    在 crawlib 中一个 url 对应着一个 entity, 而 html 中可能会抓取到其他 child entity
    的信息. 对于当前 entity 的信息, 我们将其存储在 :attr:`ParseResult.entity` 中.
    对于 child entity 的信息, 我们将其存储在 :attr:`ParseResult.children` 中.

    :param entity: 由于 html 背后必然对应一个 url, 而在 crawlib2 框架里, 每一个 url
        都对应着一个 ORM Entity. 此属性保存的就是这个从 html 中提取出来的,
        跟 html 唯一对应的 Entity 的其他属性.
    :param children: 从 entity 所对应的 url 页面上抓取下来的其他 entity 实例. 在
        ``Entity.process_pr`` 方法中, 会根据 child entity 的类型进行归类, 然后对
        每类进行处理.
    :param data: 额外的数据
    :param status: 表示当前的抓取状态
    :param enit_at: 表示最新更新的时间
    """
    entity = attr.ib(default=None)  # type: Optional[Entity]
    children = attr.ib(factory=list)  # type: Optional[List[Entity]]
    data = attr.ib(factory=dict)  # type: Dict
    status = attr.ib(
        default=Status.S30_ParseError.id,
        validator=attr.validators.instance_of(int)
    )  # type: int
    edit_at = attr.ib(default=datetime.utcnow())  # type: datetime

    @entity.validator
    def check_entity(self, attribute, value):
        """
        - :attr:`ParseResult.entity` could be None, it means the SELF entity
            will not be updated.
        - :attr:`ParseResult.entity` should be Any subclass of :class:`Entity`
        """
        if value is not None:
            if not isinstance(value, Entity):
                raise TypeError("ParseResult.entity has to be an Entity")

    @children.validator
    def check_children(self, attribute, value):
        for item in value:
            if not isinstance(item, Entity):
                raise TypeError("ParseResult.children has to be a list of Entity")

    # -- utility methods
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
        self.status = Status.S50_Finished.id

    def set_status_server_side_error(self):
        self.status = Status.S60_ServerSideError.id

    def set_status_finalized(self):
        self.status = Status.S99_Finalized.id

    def is_finished(self):
        """
        test if the status should be marked as `finished`.

        :rtype: bool
        """
        try:
            return self.status >= FINISHED_STATUS_CODE
        except:  # pragma: no cover
            return False
