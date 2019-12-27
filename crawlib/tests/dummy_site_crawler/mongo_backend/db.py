# -*- coding: utf-8 -*-

from mongoengine import connect

from .config_init import config

uri = "mongodb://{username}:{password}@{host}:{port}/{database}".format(
    database=config.DB_DATABASE.get_value(),
    host=config.DB_HOST.get_value(),
    port=config.DB_PORT.get_value(),
    username=config.DB_USERNAME.get_value(),
    password=config.DB_PASSWORD.get_value(),
)
print(uri)
client = connect(
    db=config.DB_DATABASE.get_value(),
    host=uri,
    alias=config.DB_DATABASE.get_value(),
    retryWrites=False,
)
db = client[config.DB_DATABASE.get_value()]
