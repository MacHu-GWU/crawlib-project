# -*- coding: utf-8 -*-

from flask import Flask


def create_app():
    from . import (
        movie,
        music,
    )

    app = Flask("app")
    bp_list = [
        movie,
        music
    ]
    for bp in bp_list:
        app.register_blueprint(bp)

    return app
