"""
Module text goes here.
"""
import gzip
import json
from flask import Response, request, Blueprint, render_template
from time import perf_counter

from .queries import get_all_sets
from .database_session import DatabaseSession
from .database import Database
from .routes_utils import build_rows, get_encoding, replace_placeholders

bp = Blueprint('main', __name__, template_folder="templates")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/sets")
def sets():
    encoding = get_encoding(request)
    meta_charset = '<meta charset="UTF-8">' if encoding == "utf-8" else ""

    with open("app/templates/sets.html", "r", encoding="utf-8") as f:
        template = f.read()

    with DatabaseSession() as session:
        start_time = perf_counter()
        db = Database(session)
        result = db.fetch_all(get_all_sets())
        rows = build_rows(result)
        print(f"Time to render all sets: {perf_counter() - start_time}")

    page_html = replace_placeholders(template, meta_charset, rows)
    encoded_html = page_html.encode(encoding)
    compressed_html = gzip.compress(encoded_html)

    return Response(compressed_html,
                    content_type=f"text/html; charset={encoding}",
                    headers={"Content-Encoding": "gzip"})


@bp.route("/set")
def lego_set():  # We don't want to call the function `set`, that would hide the `set` data type.
    return render_template("set.html")


@bp.route("/api/set")
def api_set():
    set_id = request.args.get("id")
    result = {"set_id": set_id}
    json_result = json.dumps(result, indent=4)
    return Response(json_result, content_type="application/json")
