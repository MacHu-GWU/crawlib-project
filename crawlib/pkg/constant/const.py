#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
try:
    from .pkg import pylru
    from .pkg.sixmini import integer_types, string_types
except:
    from constant.pkg import pylru
    from constant.pkg.sixmini import integer_types, string_types


def get_attributes(klass):
    """Get all class attributes.
    """
    attributes = list()
    for attr, _ in inspect.\
            getmembers(klass, lambda x: not inspect.isroutine(x)):
        if not (attr.startswith("__") and attr.endswith("__")):
            attributes.append(attr)
    return attributes


class Constant(object):

    """A constant data collection.
    """

    @classmethod
    def items(cls):
        """Attributes ordered by alphabetical order.
        """
        l = list()
        for attr in get_attributes(cls):
            value = cls.__dict__[attr]
            try:
                if not issubclass(value, Constant):
                    l.append((attr, value))
            except:
                l.append((attr, value))
        return l

    @classmethod
    def keys(cls):
        return [attr for attr, _ in cls.items()]

    @classmethod
    def values(cls):
        return [value for _, value in cls.items()]

    @classmethod
    def to_dict(cls):
        return dict(cls.items())

    @classmethod
    def collection(cls, sort_by=None, reverse=False):
        """Sub class ordered by alphabetical order.
        """
        l = list()
        for attr in get_attributes(cls):
            value = cls.__dict__[attr]
            try:
                if issubclass(value, Constant):
                    l.append(value)
            except:
                pass
        if sort_by is not None:
            l = list(
                sorted(l, key=lambda x: getattr(x, sort_by), reverse=reverse))
        return l

    @classmethod
    @pylru.lrudecorator(32)
    def get(cls, attr, value, multi=False, e=0.000001):
        """Get a subclass that subclass.attr == value.

        :param multi: if True, then return all matched.
        :param e: used for float value comparison.
        """
        if multi:
            matched = list()
            for klass in cls.collection():
                d = klass.__dict__
                try:
                    if isinstance(value, integer_types):
                        try:
                            if d[attr] == value:
                                matched.append(klass)
                        except:
                            pass
                    elif isinstance(value, float):
                        try:
                            if abs(d[attr] - value) <= e:
                                matched.append(klass)
                        except:
                            pass
                    elif isinstance(value, string_types):
                        try:
                            if d[attr] == value:
                                matched.append(klass)
                        except:
                            pass
                    else:
                        try:
                            if d[attr] == value:
                                matched.append(klass)
                        except:
                            pass
                except:
                    pass

            return matched

        else:
            for klass in cls.collection():
                d = klass.__dict__
                try:
                    if isinstance(value, integer_types):
                        try:
                            if d[attr] == value:
                                return klass
                        except:
                            pass
                    elif isinstance(value, float):
                        try:
                            if abs(d[attr] - value) <= e:
                                return klass
                        except:
                            pass
                    elif isinstance(value, string_types):
                        try:
                            if d[attr] == value:
                                return klass
                        except:
                            pass
                    else:
                        try:
                            if d[attr] == value:
                                return klass
                        except:
                            pass
                except:
                    pass

            return None
