# -*- coding: utf-8 -*-

from configirl import ConfigClass, Constant, Derivable


class Config(ConfigClass):
    DB_LOCAL_HOST = Constant(default="localhost")
    DB_LOCAL_PORT = Constant(default=43346)
    DB_LOCAL_DATABASE = Constant(default="admin")
    DB_LOCAL_USERNAME = Constant(default="username")
    DB_LOCAL_PASSWORD = Constant(default="password")

    DB_HOST = Derivable()

    @DB_HOST.getter
    def get_DB_HOST(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_HOST.get_value()
        else:
            return self.DB_LOCAL_HOST.get_value()

    DB_PORT = Derivable()

    @DB_PORT.getter
    def get_DB_PORT(self):
        if self.is_ci_runtime():
            return 27017
        else:
            return self.DB_LOCAL_PORT.get_value()

    DB_DATABASE = Derivable()

    @DB_DATABASE.getter
    def get_DB_DATABASE(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_DATABASE.get_value()
        else:
            return self.DB_LOCAL_DATABASE.get_value()

    DB_USERNAME = Derivable()

    @DB_USERNAME.getter
    def get_DB_USERNAME(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_USERNAME.get_value()
        else:
            return self.DB_LOCAL_USERNAME.get_value()

    DB_PASSWORD = Derivable()

    @DB_PASSWORD.getter
    def get_DB_PASSWORD(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_PASSWORD.get_value()
        else:
            return self.DB_LOCAL_PASSWORD.get_value()
