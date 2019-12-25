# -*- coding: utf-8 -*-

from flask import Flask


def create_app():
    from . import (
        _index,
        movie,
        music,
    )

    app = Flask(__name__)
    app.register_blueprint(_index.bp)
    app.register_blueprint(movie.bp, url_prefix="/movie")
    app.register_blueprint(music.bp, url_prefix="/music")

    return app
