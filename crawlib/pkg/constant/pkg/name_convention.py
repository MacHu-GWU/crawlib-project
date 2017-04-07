#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
else:
    string_types = basestring,
    integer_types = (int, long)

SEP = "____"
KLS_NAME_CHARSET = set(string.ascii_letters + string.digits)
VAR_NAME_CHARSET = set(string.ascii_lowercase + string.digits + "_")
VAR_FORBIDDEN_CHARSET = set(r"""~`!@#$%^&*()-+={}[]|\:;"'<,>.?/""" + string.ascii_uppercase)
INDEX_KEY_FORBIDDEN_CHARSET = set(r"""~`!@#$%^&*()-+={}[]|\:;"'<,>.?/""")
WHITE_SPACE = set(string.whitespace)


def is_valid_class_name(name):
    """Check if it is a valid variable name.
    
    A valid variable name has to:
    
    - start wither upper case
    - only alpha digits
    """
    try:
        assert name[0].isupper()
        assert len(set(name).difference(KLS_NAME_CHARSET)) == 0
        return True
    except:
        return False


def is_valid_variable_name(name):
    """Check if it is a valid variable name.
    
    A valid variable name has to:
    
    - start wither lower case
    - reserved SEPTERATOR is not in it.
    """
    try:
        assert name[0].islower()
        assert SEP not in name
        assert len(set(name).difference(VAR_NAME_CHARSET)) == 0
        return True
    except:
        return False


def is_valid_surfix(name):
    """Surfix is the attribute name used for index.
    
    **中文文档**
    
    此方法暂时没用。
    """
    try:
        assert SEP not in name
        assert len(VAR_FORBIDDEN_CHARSET.intersection(name)) == 0
        return True
    except:
        return False
    
    
def to_variable_name(cls_name):
    """Convert class name to variable name format. usually use "_" to connect
    each word.
    
    **中文文档**
    
    将类名转化为其实例的变量名。
    """
    assert is_valid_class_name(cls_name)

    words = list()
    chunks = list()
    for char in cls_name:
        if char.isupper():
            words.append("".join(chunks))
            chunks = ["_", char.lower()]
        else:
            chunks.append(char)
    words.append("".join(chunks))
    return "".join(words)[1:]


def to_index_key(value):
    """Convert a value to it's index key in string.
    Only alpha and digits and underscore is allowed. Whitespace delimiter will
    replaced with underscore.
    
    ``  *David#   #John* `` -> ``David_John``
    """
    if isinstance(value, integer_types):
        key = str(value)
    
    elif isinstance(value, string_types):
        l = list()
        for c in value:
            if c not in INDEX_KEY_FORBIDDEN_CHARSET:
                if c in WHITE_SPACE:
                    l.append(" ")
                else:
                    l.append(c)
        words = [word for word in "".join(l).strip().split(" ") if word.strip()]
        key = "_".join(words)
    
    elif isinstance(value, float):
        key = str(value).replace(".", "d")
        
    else:
        raise TypeError("%r is not an indexable value.")
    
    return key 

    
def test_is_valid_class_name():
    for name in ["User", "MyClass", "TestCase"]:
        assert is_valid_class_name(name) is True

    for name in ["user", "My_Class", "testCase"]:
        assert is_valid_class_name(name) is False


def test_is_valid_variable_name():
    for name in ["name", "my_class", "num1"]:
        assert is_valid_variable_name(name) is True

    for name in ["Name", "myClass", "1a"]:
        assert is_valid_variable_name(name) is False


def test_is_valid_surfix():
    assert is_valid_surfix("大卫") is True
    

def test_to_variable_name():
    assert to_variable_name("User") == "user"
    assert to_variable_name("MyClass") == "my_class"


def test_to_index_key():
    assert to_index_key(1) == "1"
    assert to_index_key("David John") == "David_John"
    assert to_index_key("  *David+  +John*  ") == "David_John"
    assert to_index_key("中文") == "中文"
    assert to_index_key(" 英 文 ") == "英_文"
    assert to_index_key(3.14) == "3d14"
    
 
if __name__ == "__main__":
    test_is_valid_class_name()
    test_is_valid_variable_name()
    test_is_valid_surfix()
    test_to_variable_name()
    test_to_index_key()