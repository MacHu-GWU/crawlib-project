#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import connect

dbname = "devtest"
username = "admin"
password = "&2z7#tMH6BJt"


def connect_mlabs():
    host = "mongodb://{username}:{password}@ds113063.mlab.com:13063/devtest". \
        format(username=username, password=password)
    client = connect(dbname, alias=dbname, host=host)
    client.drop_database(dbname)
    db = client[dbname]
    return client, db


def connect_mongomock():
    client = connect(dbname, alias=dbname, host="mongomock://localhost")
    client.drop_database(dbname)
    db = client[dbname]
    return client, db


# client, db = connect_mongomock()
client, db = connect_mlabs()
