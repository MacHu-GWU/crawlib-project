#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loggerFactory import StreamOnlyLogger
from crawlib import SpiderLogger

logger = SpiderLogger(logger=StreamOnlyLogger())
