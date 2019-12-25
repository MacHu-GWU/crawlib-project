# -*- coding: utf-8 -*-

"""
- /movie-listpage/
- /movie-listpage/<page_id>
- /movie/<movie_id>
"""

import math
from flask import Flask, Blueprint, render_template

bp = Blueprint("movie", __name__, template_folder="templates")

app = Flask("movie")

n_movie = 98
n_movie_each_page = 10
max_page_id = math.ceil(n_movie * 1.0 / n_movie_each_page)


@bp.route("/movie", methods=["GET", ])
def index():
    return render_template("index.html")


@bp.route("/movie/listpage/", methods=["GET", ])
@bp.route("/movie/listpage/<page_id>", methods=["GET", ])
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
            movie_id_list = [
                (page_id - 1) * n_movie_each_page + 1 + i
                for i in range(n_movie_each_page)
            ]
            next_page_id = page_id + 1
        elif page_id > max_page_id:
            raise ValueError
        else:
            movie_id_list = list(range(
                (page_id - 1) * n_movie_each_page + 1, n_movie + 1
            ))
            next_page_id = max_page_id
        return render_template(
            "movie-listpage.html",
            movie_id_list=movie_id_list,
            prev_page_id=prev_page_id,
            next_page_id=next_page_id,
            last_page_id=max_page_id,
        )


@bp.route("/movie/<movie_id>", methods=["GET", ])
def movie_detail(movie_id):
    return render_template("movie.html", movie_id=movie_id)


if __name__ == "__main__":
    from crawlib.tests.dummy_site.config import PORT

    app = Flask("movie")
    app.register_blueprint(bp)
    app.run(port=PORT, debug=True)
