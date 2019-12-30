# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple, Type, Union, Iterable

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy_mate import ExtendedBase
from sqlalchemy_mate.crud.updating import update_all

from ..base import Entity, ParseResult, Relationship
from ...status import FINISHED_STATUS_CODE
from ...status import Status
from ...time_util import epoch, x_seconds_before_now

Base = declarative_base()


class SqlEntity(ExtendedBase, Entity):
    """

    **中文文档**

    """
    _ORM_FRAMEWORK = "sqlalchemy"

    @classmethod
    def _pre_process_only_fields_arg(cls,
                                     only_fields: List[Union[sa.Column, str]]) -> Tuple[
        bool, List[str], List[sa.Column]]:
        """
        What does this method do?

        Because sqlalchemy ORM query api returns different type based on the
        argument of session.query(...). If the argument is a ORM class, it returns
        a iterable object can yield lots of data model instance. If the argument
        is a bunch of ORM attributes (such as ``session.query(User.id, User.name)``)
        it returns a iterable object can yield lots of ``namedtuples``. In this
        framework, we only need to retrieve part of the column to start crawling.

        This method analysis ``only_fields`` argument, identify if it is a
        partial load. And returns the list of columns and its names that we only
        need.

        :param only_fields:
        :return:

        **中文文档**

        由于 sqlalchemy ORM query API 的返回值会根据 query 方法的参数而有所不同. 如果
        session.query(...) 的参数是一个类, 则行为是返回所有 column 中的数据, 并返回
        data model instance. 而如果参数是多个类属性, 则行为是返回一个 tuple, 只
        包含指定 column 中的数据. 这会影响后续的 API 一致性. 而在本爬虫框架中我们通常
        只需要部分 column 中的数据用于 build url. 所以我们往往会使用后一种参数.

        本方法的功能是, 分析 `only_fields` 参数, 判断是否是 partial load, 并把 flag
        复制给 ``is_partial_load``, 可以用它来判断 query 方法的返回值类型. 以及返回
        所有被选择的 sa.Column.name 的列表, 和 sa.Column 的对象的列表.
        """
        if only_fields is None:
            if cls.CONF_ONLY_FIELDS is None:
                is_partial_load = False
            else:
                is_partial_load = True
                only_fields = cls.CONF_ONLY_FIELDS
        else:
            is_partial_load = True

        if is_partial_load:
            only_column_names, only_column_objects = list(), list()
            for field_or_field_name in only_fields:
                if isinstance(field_or_field_name, str):
                    only_column_names.append(field_or_field_name)
                    only_column_objects.append(getattr(cls, field_or_field_name))
                else:
                    only_column_names.append(field_or_field_name.name)
                    only_column_objects.append(field_or_field_name)
        else:
            only_column_names, only_column_objects = list(), list()

        return (
            is_partial_load,
            only_column_names,
            only_column_objects,
        )

    @classmethod
    def _build_query_to_get_unfinished_or_finished(cls,
                                                   is_finished: bool,
                                                   session: Session,
                                                   filters: Union[
                                                       List[BinaryExpression], Tuple[BinaryExpression]] = None,
                                                   only_fields: Union[
                                                       List[sa.Column], Tuple[sa.Column]] = None,
                                                   limit: int = None,
                                                   **kwargs) -> Tuple[bool, Query]:
        """
        Build sqlalchemy ORM query object from arguments.
        """
        # query() args
        (
            is_partial_load,
            only_column_names,
            only_column_objects,
        ) = cls._pre_process_only_fields_arg(only_fields)

        if is_partial_load:
            query = session.query(*only_column_objects)
        else:
            query = session.query(cls)

        # filter() args
        if is_finished:
            final_filters = [
                getattr(cls, cls.CONF_STATUS_KEY) >= FINISHED_STATUS_CODE,
                getattr(cls, cls.CONF_EDIT_AT_KEY) >= x_seconds_before_now(cls.CONF_UPDATE_INTERVAL),
            ]
        else:
            final_filters = [
                sa.or_(
                    getattr(cls, cls.CONF_STATUS_KEY) < FINISHED_STATUS_CODE,
                    getattr(cls, cls.CONF_EDIT_AT_KEY) < x_seconds_before_now(cls.CONF_UPDATE_INTERVAL),
                )
            ]
        if (filters is not None) and isinstance(filters, (list, tuple)):
            for criterion in filters:
                final_filters.append(criterion)
        query = query.filter(sa.and_(*final_filters))

        if limit is not None:
            query = query.limit(limit)
        return (is_partial_load, query)

    @classmethod
    def get_unfinished(cls,
                       session: Session,
                       filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                       only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                       limit: int = None,
                       **kwargs) -> Union[Query, Iterable['SqlEntity']]:
        """
        Execute a query to get all **Not Finished** web page ORM entity

        :param session: sqlalchemy orm Session object.
        :param filters: additional sqlalchemy ORM filter. By default it use
            AND operator.
        :param only_fields: if specified, only returns seleted columns.
        :param limit: limit the number of entity to return

        :return: an iterable object of ORM entities
        """
        is_partial_load, query = cls._build_query_to_get_unfinished_or_finished(
            is_finished=False,
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        )

        if is_partial_load:
            return [
                cls(**row._asdict())
                for row in query
            ]
        else:
            return list(query)

    @classmethod
    def count_unfinished(cls,
                         session: Session,
                         filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                         only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                         limit: int = None,
                         **kwargs) -> int:
        """
        Just count
        :param session:
        :param filters:
        :param only_fields:
        :param limit:
        :param kwargs:
        :return:
        """
        return cls._build_query_to_get_unfinished_or_finished(
            is_finished=False,
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        )[1].count()

    @classmethod
    def get_finished(cls,
                     session: Session,
                     filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                     only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                     limit: int = None,
                     **kwargs) -> Union[Query, Iterable]:  # pragma: no cover
        """
        Execute a query to get all **Finished** web page ORM entity

        :param session: sqlalchemy orm Session object.
        :param filters: additional sqlalchemy ORM filter. By default it use
            AND operator.
        :param only_fields: if specified, only returns seleted columns.
        :param limit: limit the number of entity to return

        :return: an iterable object of ORM entities
        """
        is_partial_load, query = cls._build_query_to_get_unfinished_or_finished(
            is_finished=True,
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        )

        if is_partial_load:
            return [
                cls(**row._asdict())
                for row in query
            ]
        else:
            return list(query)

    @classmethod
    def count_finished(cls,
                       session: Session,
                       filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                       only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                       limit: int = None,
                       **kwargs) -> int:
        return cls._build_query_to_get_unfinished_or_finished(
            is_finished=True,
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        )[1].count()

    @classmethod
    def validate_implementation_additional(cls):
        """
        SQL Backend specified implementation check.

        1. the status column has to be ``sqlalchemy.Integer`` type
        2. the edit at column has has to be ``sqlalchemy.DateTime`` type
        3. if it has relation ``one-to-many``, then the
        """
        try:
            status_column = getattr(cls, cls.CONF_STATUS_KEY)  # type: sa.Column
            if not isinstance(status_column.type, sa.Integer):
                raise NotImplementedError(
                    "`{}.{}` column has to be a `sqlalchemy.Column(sqlalchemy.Integer, ...)`!".format(
                        cls.__name__, status_column
                    ))
        except:
            raise NotImplementedError("status column (a sqlalchemy.Column) not found!")

        try:
            edit_at_column = getattr(cls, cls.CONF_EDIT_AT_KEY)  # type: sa.Column
            if not isinstance(edit_at_column.type, sa.DateTime):
                raise NotImplementedError(
                    "`{}.{}` column has to be a `sqlalchemy.Column(sqlalchemy.DateTime, ...)`!".format(
                        cls.__name__, edit_at_column
                    ))
        except:
            raise NotImplementedError(
                "edit at column (a sqlalchemy.Column) not found!")

        for klass in cls.CONF_RELATIONSHIP.mapping:
            if cls.CONF_RELATIONSHIP.get_relationship(klass) == Relationship.Option.many:
                n_child_key = cls.CONF_RELATIONSHIP.get_n_child_key(klass)
                if hasattr(cls, n_child_key) is False:
                    msg = "{} does not define '{}' column!".format(cls, n_child_key)
                    raise NotImplementedError(msg)
                n_child_column = getattr(cls, n_child_key)  # type: sa.Column
                if not isinstance(n_child_column.type, sa.Integer):
                    raise NotImplementedError(
                        "`{}` column has to be a `sqlalchemy.Column(sqlalchemy.Integer, ...)`!".format(n_child_key))

    def set_db_values(self,
                      data: dict,
                      engine: sa.engine.Engine,
                      upsert: bool = True,
                      **kwargs) -> None:
        """
        :param data:
        :param session:
        :param kwargs:
        :return:

        **中文文档**

        使用当前实例的 primary key 的值定位到对应 row, 并使用 data 中的数据对其进行
        更新. 当前实例的 primary key 必须有值.

        之所单独创建一个方法的原因是, sqlalchemy.DeclartiveBase.update 方法无法给予
        我们精细的控制, 因为你必须要维护一个 instance, 而 instance 其他无关的 column 的
        初始值需要我们手动处理, 以防这些初始值被更新到数据库. 所以选择使用原生 sql API
        根据 primary_key 的值对指定的几个 column 进行更新.
        """
        id_field_name = self.__class__.id_field_name()
        id_field_value = self.id_field_value()
        table = self.__class__.__table__
        upd = table.update().where(
            getattr(table.c, id_field_name) == id_field_value
        ).values(**data)
        result = engine.execute(upd)
        if (result.rowcount == 0) and (upsert is True):
            ins = table.insert()
            data[id_field_name] = id_field_value
            engine.execute(ins, data)

    def process_pr(self,
                   pres: ParseResult,
                   engine,
                   **kwargs):
        """
        Process ParseRequest

        :param pres: parse result object to process

        **中文文档**

        **注意! 理解 update parent entity 的行为**:

        在 sqlalchemy ORM 框架中, 如果定义了 ``sa.Column(..., default=some_value)``
        这里有一个坑. 其他框架如 attrs, mongoengine 会在你初始化对象时, 就会将默认值
        赋值给对象. 也就是说你用 形如 ``user.name`` 的方式访问到的是默认值. **而 sqlalchemy
        框架中并不会将默认值赋值给对象, 而是在执行 insert / update 时将默认值写入数据库**

        我们在 update parent entity 时实际上是在更新 URL 页面上抓取到的跟 entity 有关
        的信息. 如果我们用 User(id=1)
        """
        if pres.is_finished():
            # disaggregate child entiity, group them by class
            # CN doc: pres.children 中可能有多余两类的对象, 我们首先将其按照类分组
            entity_bags = dict()  # type: Dict[Type[SqlEntity], List[SqlEntity]]
            for child in pres.children:
                try:
                    entity_bags[child.__class__].append(child)
                except KeyError:
                    entity_bags[child.__class__] = [child, ]

            # insert child entity, update n_child_key attribute in parent entity
            # 将新获得的 child entity 插入数据库, 并更新 n_child_key
            for entity_klass, entity_list in entity_bags.items():
                entity_klass.smart_insert(engine, entity_list)
                n_child = len(entity_list)
                n_child_key = self.CONF_RELATIONSHIP.get_n_child_key(entity_klass)
                if pres.entity_data is not None:
                    pres.entity_data[n_child_key] = n_child

        # update parent entity in db
        if pres.entity_data is not None:
            pres.entity_data[self.CONF_STATUS_KEY] = pres.status
            pres.entity_data[self.CONF_EDIT_AT_KEY] = pres.edit_at
            self.set_db_values(pres.entity_data, engine, upsert=False)


class SqlEntitySingleStatus(SqlEntity):
    CONF_STATUS_KEY = "status"
    CONF_EDIT_AT_KEY = "edit_at"

    status = sa.Column(sa.Integer, default=Status.S0_ToDo.id)
    edit_at = sa.Column(sa.DateTime, default=epoch)
