# -*- coding: utf-8 -*-

import random
from collections import OrderedDict

from pathlib_mate import Path
from flask import Flask, Blueprint, render_template

dir_templates = Path(__file__).change(new_basename="templates")
bp = Blueprint("music", __name__, template_folder=dir_templates.abspath)

n_artist = 15
n_genre = 10
n_music = 50

max_n_artist = 3
max_n_genre = 2

artists = OrderedDict([
    (artist_id, {"id": artist_id, "music_id_list": []})
    for artist_id in range(1, 1 + n_artist)
])
artist_id_list = list(artists)

genres = OrderedDict([
    (genre_id, {"id": genre_id, "music_id_list": []})
    for genre_id in range(1, 1 + n_genre)
])
genre_id_list = list(genres)

musics = OrderedDict([
    (music_id, {"id": music_id, "artist_id_list": [], "genre_id_list": []})
    for music_id in range(1, 1 + n_music)
])

music_id_list = list(musics)

for music_id, music in musics.items():
    for artist_id in random.sample(artist_id_list, max_n_artist):
        music["artist_id_list"].append(artist_id)
        artists[artist_id]["music_id_list"].append(music_id)
    for genre_id in random.sample(genre_id_list, max_n_genre):
        music["genre_id_list"].append(genre_id)
        genres[genre_id]["music_id_list"].append(music_id)

n_random_music = 5


@bp.route("/", methods=["GET", ])
def index():
    print("Music page")
    return render_template("music/index.html")


@bp.route("/random", methods=["GET", ])
def random_music():
    _music_id_list = random.sample(music_id_list, n_random_music)
    _music_id_list.sort()
    return render_template("music/random.html", music_id_list=_music_id_list)


@bp.route("/<music_id>", methods=["GET", ])
def music_detail(music_id):
    return render_template("music/music.html", music=musics[int(music_id)])


@bp.route("/artist/<artist_id>", methods=["GET", ])
def artist_detail(artist_id):
    return render_template("music/artist.html", artist=artists[int(artist_id)])


@bp.route("/genre/<genre_id>", methods=["GET", ])
def genre_detail(genre_id):
    return render_template("music/genre.html", genre=genres[int(genre_id)])


if __name__ == "__main__":
    from crawlib.tests.dummy_site.config import PORT

    app = Flask("music")
    app.register_blueprint(bp, url_prefix="/music")
    app.run(port=PORT, debug=True)
