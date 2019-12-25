# -*- coding: utf-8 -*-

import random
from collections import OrderedDict

from flask import Flask, Blueprint, render_template

bp = Blueprint("music", __name__, template_folder="templates")

n_artist = 50
n_genre = 30
n_music = 500

max_n_artist = 2
max_n_genre = 3

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

n_random_music = 10


@bp.route("/music", methods=["GET", ])
def index():
    return render_template("index.html")


@bp.route("/music/random", methods=["GET", ])
def random_music():
    _music_id_list = random.sample(music_id_list, n_random_music)
    _music_id_list.sort()
    return render_template("random.html", music_id_list=_music_id_list)


@bp.route("/music/<music_id>", methods=["GET", ])
def music_detail(music_id):
    return render_template("music.html", music=musics[int(music_id)])


@bp.route("/music/artist/<artist_id>", methods=["GET", ])
def artist_detail(artist_id):
    return render_template("artist.html", artist=artists[int(artist_id)])


@bp.route("/music/genre/<genre_id>", methods=["GET", ])
def genre_detail(genre_id):
    return render_template("genre.html", genre=genres[int(genre_id)])


if __name__ == "__main__":
    from crawlib.tests.dummy_site.config import PORT

    app = Flask("music")
    app.register_blueprint(bp)
    app.run(port=PORT, debug=True)
