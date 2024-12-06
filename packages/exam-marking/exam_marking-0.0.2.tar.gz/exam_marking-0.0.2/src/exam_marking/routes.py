import sqlite3
from itertools import zip_longest

from flask import Blueprint, g, render_template, request

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    first_unmarked = None
    for row in g.marks:
        if all(m is None for m in row["marks"]):
            first_unmarked = row["zid"]
            break
    return render_template(
        "index.html",
        zip_longest=zip_longest,
        enumerate=enumerate,
        first_unmarked=first_unmarked,
    )


@bp.route("/change", methods=["POST"])
def change():
    zid = request.form.get("zid")
    marks = []
    for i, col in enumerate(g.columns):
        marks.append(request.form.get(f"marks-{i}"))

    for row in g.marks:
        if row["zid"] == zid:
            row["marks"] = [m if m is not None else 0 for m in marks]

    return "", 204
