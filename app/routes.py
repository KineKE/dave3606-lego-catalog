"""
Module text goes here.
"""

import json
import html
from flask import Response, request, Blueprint, render_template, jsonify
from time import perf_counter

from . import queries
from .database_session import DatabaseSession
from .database import Database

bp = Blueprint('main', __name__, template_folder="templates")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/sets")
def sets():
    with open("app/templates/sets.html") as f:
        template = f.read()

    with DatabaseSession() as session:
        start_time = perf_counter()
        db = Database(session)
        result = db.fetch_all(queries.get_all_sets())

        rows = []
        for row in result:
            html_safe_id = html.escape(row[0])
            html_safe_name = html.escape(row[1])

            rows.append(
                f'<tr><td><a href="/set?id={html_safe_id}">{html_safe_id}</a></td><td>{html_safe_name}</td></tr>\n'
            )

        rows = "\n".join(rows)
        print(f"Time to render all sets: {perf_counter() - start_time}")

    page_html = template.replace("{ROWS}", rows)
    return Response(page_html, content_type="text/html")


@bp.route("/set")
def lego_set():  # We don't want to call the function `set`, since that would hide the `set` data type.
    return render_template("set.html")


@bp.route("/api/set")
def api_set():
    set_id = request.args.get("id")
    result = {"set_id": set_id}
    json_result = json.dumps(result, indent=4)
    return Response(json_result, content_type="application/json")
