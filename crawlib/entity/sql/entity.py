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


class SqlEntity(Base, ExtendedBase, Entity):
    __abstract__ = True

    @classmethod
    def get_unfinished(cls,
                       session: Session,
                       filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                       only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                       limit: int = None,
                       **kwargs) -> Union[Query, Iterable]:
        """
        Execute a query to get all **Not Finished** web page ORM entity

        :param session: sqlalchemy orm Session object.
        :param filters: additional sqlalchemy ORM filter. By default it use
            AND operator.
        :param only_fields: if specified, only returns seleted columns.
        :param limit: limit the number of entity to return

        :rtype:
        """
        default_filters = [
            getattr(cls, cls.CONF_STATUS_KEY) < FINISHED_STATUS_CODE,
            getattr(cls, cls.CONF_EDIT_AT_KEY) < x_seconds_before_now(cls.CONF_UPDATE_INTERVAL),
        ]
        final_filters = list()
        final_filters.append(sa.or_(*default_filters))
        if (filters is not None) and isinstance(filters, (list, tuple)):
            for criterion in filters:
                final_filters.append(criterion)

        if only_fields is None:
            resultset = session.query(cls).filter(sa.and_(*final_filters))
        elif isinstance(only_fields, (list, tuple)):
            resultset = session.query(*only_fields).filter(sa.and_(*final_filters))
        else:
            raise TypeError

        if limit is not None:
            resultset = resultset.limit(limit)

        return resultset

    @classmethod
    def count_unfinished(cls,
                         session: Session,
                         filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                         only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                         limit: int = None,
                         **kwargs) -> int:
        return cls.get_unfinished(
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        ).count()

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
        """
        final_filters = [
            getattr(cls, cls.CONF_STATUS_KEY) >= FINISHED_STATUS_CODE,
            getattr(cls, cls.CONF_EDIT_AT_KEY) >= x_seconds_before_now(cls.CONF_UPDATE_INTERVAL),
        ]
        if (filters is not None) and isinstance(filters, (list, tuple)):
            for criterion in filters:
                final_filters.append(criterion)

        if only_fields is None:
            resultset = session.query(cls).filter(sa.and_(*final_filters))
        elif isinstance(only_fields, (list, tuple)):
            resultset = session.query(*only_fields).filter(sa.and_(*final_filters))
        else:
            raise TypeError

        if limit is not None:
            resultset = resultset.limit(limit)

        return resultset

    @classmethod
    def count_finished(cls,
                       session: Session,
                       filters: Union[List[BinaryExpression], Tuple[BinaryExpression]] = None,
                       only_fields: Union[List[sa.Column], Tuple[sa.Column]] = None,
                       limit: int = None,
                       **kwargs) -> int:
        return cls.get_finished(
            session=session,
            filters=filters,
            only_fields=only_fields,
            limit=limit,
            **kwargs
        ).count()

    @classmethod
    def validate_implementation_additional(cls):
        """
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

    def process_pr(self,
                   pres: ParseResult,
                   **kwargs):
        """
        Process ParseRequest

        :param pres: parse result object to process

        :return:
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
                entity_klass.smart_insert(entity_list)
                n_child = len(entity_list)
                n_child_key = self.CONF_RELATIONSHIP.get_n_child_key(entity_klass)
                if pres.entity is not None:
                    setattr(pres.entity, n_child_key, n_child)

        # update parent entity in db
        if pres.entity is not None:
            setattr(pres.entity, self.id_field_name(), getattr(self, self.id_field_name()))
            setattr(pres.entity, self.CONF_STATUS_KEY, pres.status)
            setattr(pres.entity, self.CONF_EDIT_AT_KEY, pres.edit_at)
            entity_data_to_update = pres.entity.filter_update_data()
            update_one_response = update_all(
                engine=kwargs["engine"],
                table=self.__table__,
                data=[entity_data_to_update, ],
            )


class SqlEntitySingleStatus(SqlEntity):
    __abstract__ = True

    CONF_STATUS_KEY = "status"
    CONF_EDIT_AT_KEY = "edit_at"

    status = sa.Column(sa.Integer, default=lambda: Status.S0_ToDo.id)
    edit_at = sa.Column(sa.DateTime, default=lambda: epoch)
