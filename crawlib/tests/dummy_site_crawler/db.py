# -*- coding: utf-8 -*-

from mongoengine import connect
from .config import Config


def connect_mongomock():
    client = connect(
        Config.MongoDB.database,
        alias=Config.MongoDB.database,
        host="mongomock://localhost",
    )
    client.drop_database(Config.MongoDB.database)
    db = client[Config.MongoDB.database]
    return client, db


def connect_local():
    client = connect(
        Config.MongoDB.database,
        alias=Config.MongoDB.database,
    )
    client.drop_database(Config.MongoDB.database)
    db = client[Config.MongoDB.database]
    return client, db


client, db = connect_mongomock()
# client, db = connect_local()
