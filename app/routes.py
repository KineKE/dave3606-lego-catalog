"""
Module text goes here.
"""
import gzip
import json
from flask import Response, request, Blueprint, render_template
from time import perf_counter

from .cache import LRUCache
from .kine import build_kine_bytes
from .queries import get_all_sets, get_set_with_inventory
from .database_session import DatabaseSession
from .database import Database
from .routes_utils import (build_rows,
                           get_encoding,
                           replace_placeholders,
                           build_set_response,
                           return_400_missing_set_id,
                           return_404_set_not_found,
                           return_400_missing_set_id_binary,
                           return_404_set_not_found_binary)

bp = Blueprint('main', __name__, template_folder="templates")

set_cache = LRUCache()


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
                    headers={"Content-Encoding": "gzip",
                             "Cache-Control": "public, max-age=60"})


@bp.route("/set")
def lego_set():  # We don't want to call the function `set`, that would hide the `set` data type.
    return render_template("set.html")


@bp.route("/api/set")
def api_set():
    set_id = request.args.get("id")

    if not set_id:
        return return_400_missing_set_id()

    start_time = perf_counter()

    cached_data = set_cache.get(set_id)
    if cached_data is not None:
        elapsed = perf_counter() - start_time
        print(f"/api/set cache hit for {set_id}: {elapsed:.6f} seconds")
        return Response(
            json.dumps(cached_data, indent=4),
            content_type="application/json"
        )

    with DatabaseSession() as session:
        db = Database(session)
        query, params = get_set_with_inventory(set_id)
        rows = db.fetch_all(query, params)

    data = build_set_response(rows)

    if data is None:
        return return_404_set_not_found()

    set_cache.put(set_id, data)

    elapsed = perf_counter() - start_time
    print(f"/api/set cache miss for {set_id}: {elapsed:.6f} seconds")

    return Response(
        json.dumps(data, indent=4),
        content_type="application/json"
    )


@bp.route("/api/set-binary")
def api_set_binary():
    set_id = request.args.get("id")

    if not set_id:
        return return_400_missing_set_id_binary()

    with DatabaseSession() as session:
        db = Database(session)
        query, params = get_set_with_inventory(set_id)
        rows = db.fetch_all(query, params)

    data = build_set_response(rows)

    if data is None:
        return return_404_set_not_found_binary()

    binary_data = build_kine_bytes(data)

    return Response(
        binary_data,
        content_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{set_id}.kine"'
        }
    )
