# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint("index", __name__, template_folder="templates")


@bp.route("/", methods=["GET", ])
def index():
    return render_template("index/index.html")
