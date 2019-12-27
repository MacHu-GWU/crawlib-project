 # -*- coding: utf-8 -*-

from crawlib.tests.dummy_site.config import PORT

class Config:
    class MongoDB:
        host = "ds019633.mlab.com"
        port = 19633
        database = "crawlib-test-webapp"
        username = "admin"
        password = "k3nLDC^xUBcA"

    class Url:
        domain = "http://127.0.0.1:{}/movie".format(PORT)
