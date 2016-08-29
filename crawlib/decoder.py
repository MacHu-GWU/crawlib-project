#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide extended power to decode HTML you crawled.
"""

from __future__ import unicode_literals
import chardet


def smart_decode(binary, errors="strict"):
    d = chardet.detect(binary)
    encoding = d["encoding"]
    confidence = d["confidence"]
    text = binary.decode(encoding, errors=errors)
    return text, encoding, confidence


#--- Unittest ---
def test_find_encoding():
    ascii_text = "Hello World!"
    ascii = ascii_text.encode("ascii")    
    text, encoding, confidence = smart_decode(ascii)
    assert encoding == "ascii"
    
    utf8_text = "Python之禅: 1, 优美胜于丑陋; 2, 明了胜于晦涩; 3, 简洁胜于复杂..."
    utf8 = utf8_text.encode("utf-8")
    text, encoding, confidence = smart_decode(utf8)
    assert encoding == "utf-8"
    

def test_handle_errors():
    utf8_text = "欢迎来到Python-CN。本社区主要讨论Python和Web开发技术。"
    utf8 = utf8_text.encode("utf-8")
    
    
if __name__ == "__main__":
    test_find_encoding()
    test_handle_errors()