#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide extended power to decode HTML you crawled.
"""

import chardet
from . import util


def smart_decode(binary, errors="strict"):
    """
    Automatically find the right codec to decode binary data to string.

    :param binary: binary data
    :param errors: one of 'strict', 'ignore' and 'replace'
    :return: string
    """
    d = chardet.detect(binary)
    encoding = d["encoding"]
    confidence = d["confidence"]

    text = binary.decode(encoding, errors=errors)
    return text, encoding, confidence


class PerDomainDecoder(object):
    """
    Designed for automatically decoding html from binary content of an url.

    First, `chardet.detect` is very expensive in time.
    Second, usually each website (per domain) only use one encoding algorithm.

    :param domain_encoding_table: dict, key is root domain, and value is the
        domain's default encoding.
    """

    class ErrorsHandle(object):
        strict = "strict"
        ignore = "ignore"
        replace = "replace"

    def __init__(self):
        self.domain_encoding_table = dict()

    def decode(self, binary, url, encoding=None, errors="strict"):
        """
        Decode binary to string.

        :param binary: binary content of a http request.
        :param url: endpoint of the request.
        :param encoding: manually specify the encoding.
        :param errors: errors handle method.

        :return: str
        """
        if encoding is None:
            domain = util.get_domain(url)
            if domain in self.domain_encoding_table:
                encoding = self.domain_encoding_table[domain]
                html = binary.decode(encoding, errors=errors)
            else:
                html, encoding, confidence = smart_decode(
                    binary, errors=errors)
                # cache domain name and encoding
                self.domain_encoding_table[domain] = encoding
        else:
            html = binary.decode(encoding, errors=errors)

        return html


decoder = PerDomainDecoder()
