# -*- coding: utf-8 -*-

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_mate import EngineCreator

from .config_init import config

engine = EngineCreator(
    host=config.DB_HOST.get_value(),
    port=config.DB_PORT.get_value(),
    database=config.DB_DATABASE.get_value(),
    username=config.DB_USERNAME.get_value(),
    password=config.DB_PASSWORD.get_value(),
).create_postgresql_psycopg2()
Session = sessionmaker(bind=engine)
