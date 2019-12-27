# -*- coding: utf-8 -*-

"""
- /movie-listpage/
- /movie-listpage/<page_id>
- /movie/<movie_id>
"""

import math

from flask import Flask, Blueprint, render_template

bp = Blueprint("movie", __name__, template_folder="templates")

n_movie = 24
n_movie_each_page = 5
max_page_id = math.ceil(n_movie * 1.0 / n_movie_each_page)


@bp.route("/", methods=["GET", ])
def index():
    print("Hello")
    return render_template("movie/index.html")


@bp.route("/listpage/", methods=["GET", ])
@bp.route("/listpage/<page_id>", methods=["GET", ])
def movie_listpage(page_id=None):
    if page_id is None:
        return movie_listpage(page_id=1)
    else:
        page_id = int(page_id)

        # prev_page_id
        if page_id == 1:
            prev_page_id = 1
        else:
            prev_page_id = page_id - 1

        # next_page_id
        if page_id < max_page_id:
            movie_id_list = list(range(
                n_movie - page_id * n_movie_each_page + 1,
                n_movie - (page_id - 1) * n_movie_each_page + 1,
            ))[::-1]
            next_page_id = page_id + 1
        elif page_id > max_page_id:
            raise ValueError
        else:
            movie_id_list = list(range(
                1,
                n_movie - n_movie_each_page * (max_page_id - 1) + 1,
            ))[::-1]
            next_page_id = max_page_id
        return render_template(
            "movie/movie-listpage.html",
            movie_id_list=movie_id_list,
            prev_page_id=prev_page_id,
            next_page_id=next_page_id,
            last_page_id=max_page_id,
        )


@bp.route("/<movie_id>", methods=["GET", ])
def movie_detail(movie_id):
    return render_template("movie/movie.html", movie_id=movie_id)


if __name__ == "__main__":
    from crawlib.tests.dummy_site.config import PORT

    app = Flask("movie")
    app.register_blueprint(bp, url_prefix="/movie")
    app.run(port=PORT, debug=True)
