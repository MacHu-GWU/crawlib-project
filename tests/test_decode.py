#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from crawlib import decoder


def test():
    ascii_text = "Hello World!"
    ascii = ascii_text.encode("ascii")    
    text, encoding, confidence = decoder.smart_decode(ascii)
    assert encoding == "ascii"
    
    utf8_text = "Python之禅: 1, 优美胜于丑陋; 2, 明了胜于晦涩; 3, 简洁胜于复杂..."
    utf8 = utf8_text.encode("utf-8")
    text, encoding, confidence = decoder.smart_decode(utf8)
    assert encoding == "utf-8"
    

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])