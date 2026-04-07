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
                           build_400_response,
                           build_404_response,
                           build_400_response_binary,
                           build_404_response_binary,
                           return_cached_data,
                           build_sets_response, build_sets_page_html, load_template)

bp = Blueprint('main', __name__, template_folder="templates")
set_cache = LRUCache()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/sets")
def sets():
    encoding = get_encoding(request)
    meta_charset = '<meta charset="UTF-8">' if encoding == "utf-8" else ""
    template = load_template()

    with DatabaseSession() as session:
        start_time = perf_counter()
        db = Database(session)
        print(f"Time to render all sets: {perf_counter() - start_time}")
        page_html = build_sets_page_html(db, template, meta_charset)

    encoded_html = page_html.encode(encoding)
    compressed_html = gzip.compress(encoded_html)

    return build_sets_response(compressed_html, encoding)


@bp.route("/set")
def lego_set():  # We don't want to call the function `set`, that would hide the `set` data type.
    return render_template("set.html")


@bp.route("/api/set")
def api_set():
    set_id = request.args.get("id")

    if not set_id:
        return build_400_response()

    start_time = perf_counter()
    cached_data = set_cache.get(set_id)

    if cached_data is not None:
        elapsed = perf_counter() - start_time
        print(f"/api/set cache hit for {set_id}: {elapsed:.6f} seconds")
        return return_cached_data(cached_data)

    with DatabaseSession() as session:
        db = Database(session)
        query, params = get_set_with_inventory(set_id)
        rows = db.fetch_all(query, params)

    data = build_set_response(rows)

    if data is None:
        return build_404_response()

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
        return build_400_response_binary()

    with DatabaseSession() as session:
        db = Database(session)
        query, params = get_set_with_inventory(set_id)
        rows = db.fetch_all(query, params)

    data = build_set_response(rows)

    if data is None:
        return build_404_response_binary()

    binary_data = build_kine_bytes(data)

    return Response(
        binary_data,
        content_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{set_id}.kine"'
        }
    )
