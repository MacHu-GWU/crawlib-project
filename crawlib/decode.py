#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide extended power to decode HTML you crawled.
"""

import chardet


def smart_decode(binary, errors="strict"):
    d = chardet.detect(binary)
    encoding = d["encoding"]
    confidence = d["confidence"]
    text = binary.decode(encoding, errors=errors)
    return text, encoding, confidence
