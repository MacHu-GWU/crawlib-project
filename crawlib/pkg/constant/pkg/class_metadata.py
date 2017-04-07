#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
class的属性和instance的属性
---------------------------
类的属性和实例的属性是两个不同的概念。

- 类的属性在每一个实例中都存在。
- 实例属性并不一定在类中定义了。
- 在实例中修改类的属性只会影响当前实例, 而不会影响其他实例和类。

::

    class MyClass:
        class_attr = "class_attr" # 类的属性
        
        def __init__(self):
            self.attr = "attr" # 实例属性


method, staticmethod, classmethod
---------------------------------
"""

import sys
import inspect

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def get_attributes(klass):
    """Get all class attributes.
    """
    attributes = list()
    for attr, value in inspect.\
            getmembers(klass, lambda x: not inspect.isroutine(x)):
        if not (attr.startswith("__") and attr.endswith("__")):
            attributes.append(attr)
    return attributes


def get_methods(klass):
    """Get all methods, include regular, static, class method.
    """
    methods = list()
    attributes = get_attributes(klass)
    for key, value in inspect.getmembers(MyClass):
        if (not (key.startswith("__") and key.endswith("__"))) and \
                (key not in attributes):
            methods.append(key)
    return methods

# staticmethod, classmethod class is not exist PY2
if PY3:
    def get_regular_methods(klass):
        """Get regular methods.
        """
        regular_methods = list()
        for method in get_methods(klass):
            if not isinstance(object.__getattribute__(klass, method),
                              (staticmethod, classmethod)):
                regular_methods.append(method)
        return regular_methods

    def get_static_methods(klass):
        """Get static methods.
        """
        static_methods = list()
        for method in get_methods(klass):
            if isinstance(object.__getattribute__(klass, method), staticmethod):
                static_methods.append(method)
        return static_methods

    def get_class_methods(klass):
        """Get class methods.
        """
        class_methods = list()
        for method in get_methods(klass):
            if isinstance(object.__getattribute__(klass, method), classmethod):
                class_methods.append(method)
        return class_methods

#--- Unittest ---
if __name__ == "__main__":
    class MyClass(object):
        attr1 = "attribute1"
        attr2 = "attribute2"

        def method(self):
            pass

        @staticmethod
        def static_method():
            pass

        @classmethod
        def class_method(cls):
            pass

    def test_get_attributes():
        assert get_attributes(MyClass) == ["attr1", "attr2"]

    test_get_attributes()

    def test_get_methods():
        assert set(get_methods(MyClass)) == set(
            ["method", "static_method", "class_method", ])

    test_get_methods()

    if PY3:
        def test_get_regular_static_class_methods():
            assert get_regular_methods(MyClass) == ["method"]
            assert get_static_methods(MyClass) == ["static_method"]
            assert get_class_methods(MyClass) == ["class_method"]

        test_get_regular_static_class_methods()
