# -*- coding: utf-8 -*-

from mongoengine import connect
try:
    from .config import Config
except:
    from crawlib.example.scrapy_movie.config import Config


def connect_mongomock():
    client = connect(
        Config.MongoDB.database,
        alias=Config.MongoDB.database,
        host="mongomock://localhost",
    )
    client.drop_database(Config.MongoDB.database)
    db = client[Config.MongoDB.database]
    return client, db


def connect_cloud():
    client = connect(
        db=Config.MongoDB.database,
        host="mongodb://{username}:{password}@{host}:{port}/{database}".format(
            database=Config.MongoDB.database,
            host=Config.MongoDB.host,
            port=Config.MongoDB.port,
            username=Config.MongoDB.username,
            password=Config.MongoDB.password,
        ),
        alias=Config.MongoDB.database,
        retryWrites=False,
    )
    # client.drop_database(Config.MongoDB.database)
    db = client[Config.MongoDB.database]
    return client, db


# client, db = connect_mongomock()
client, db = connect_cloud()
