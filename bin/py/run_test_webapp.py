# -*- coding: utf-8 -*-

from crawlib.tests.dummy_site.app import create_app
from crawlib.tests.dummy_site.config import PORT

app = create_app()
# app.config["EXPLAIN_TEMPLATE_LOADING"] = True
app.run(port=PORT, debug=True)
