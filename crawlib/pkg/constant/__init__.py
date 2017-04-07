#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.5"
__short_description__ = "Use IDLE autocomplete feature to manage large amount of constants."
__license__ = "MIT"
__author__ = "Sanhe Hu"

try:
    from .tpl.class_def import gencode
except:
    pass

try:
    from .const import Constant
except:
    pass