#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, PackageLoader

dirpath = os.path.dirname(__file__)
parts = list()
for _ in range(20):
    if os.path.exists(os.path.join(dirpath, "__init__.py")):
        dirpath, basename = os.path.split(dirpath)
        parts.append(basename)
    else:
        break
package_name = ".".join(parts[::-1])

env = Environment(
    loader=PackageLoader(package_name, package_path="templates"),
)
t_class_def = env.get_template("class_def.txt")
t_collection_class_def = env.get_template("collection_class_def.txt")
t_code = env.get_template("code.txt")