import json
import html
from flask import Response, request
from time import perf_counter

from app.database import get_connection

def register_routes(app):
    @app.route("/")
    def index():
        template = open("app/templates/index.html").read()
        return Response(template)


@app.route("/sets")
def sets():
    template = open("app/templates/sets.html").read()
    rows = ""

    start_time = perf_counter()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("select id, name from lego_set order by id")
            for row in cur.fetchall():
                html_safe_id = html.escape(row[0])
                html_safe_name = html.escape(row[1])
                existing_rows = rows
                rows = existing_rows + f'<tr><td><a href="/set?id={html_safe_id}">{html_safe_id}</a></td><td>{html_safe_name}</td></tr>\n'
        print(f"Time to render all sets: {perf_counter() - start_time}")
    finally:
        conn.close()

    page_html = template.replace("{ROWS}", rows)
    return Response(page_html, content_type="text/html")


@app.route("/set")
def legoSet():  # We don't want to call the function `set`, since that would hide the `set` data type.
    template = open("app/templates/set.html").read()
    return Response(template)


@app.route("/api/set")
def apiSet():
    set_id = request.args.get("id")
    result = {"set_id": set_id}
    json_result = json.dumps(result, indent=4)
    return Response(json_result, content_type="application/json")
