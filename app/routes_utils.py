import html

from flask import Response, json

from .kine import build_kine_bytes
from .queries import get_set_with_inventory, get_all_sets


def build_rows(query_result):
    rows = []
    for row in query_result:
        html_safe_id = html.escape(row[0])
        html_safe_name = html.escape(row[1])

        rows.append(
            f'<tr>'
            f'  <td>'
            f'      <a href="/set?id={html_safe_id}">{html_safe_id}</a>'
            f'  </td>'
            f'  <td>{html_safe_name}</td>'
            f'</tr>\n'
        )

    return "\n".join(rows)


def replace_placeholders(template, meta_charset, rows):
    """
    Replace known placeholder markers in the HTML template with generated content.
    """

    return (template
            .replace("{META_CHARSET}", meta_charset)
            .replace("{ROWS}", rows))


def get_encoding(request):
    encoding = request.args.get("encoding", "utf-8").lower()

    if encoding not in {"utf-8", "utf-16"}:
        encoding = "utf-8"

    return encoding


def build_set_response(rows):
    if not rows:
        return None

    first_row = rows[0]

    set_data = {
        "id": first_row[0],
        "name": first_row[1],
        "year": first_row[2],
        "category": first_row[3],
    }

    inventory = []
    for row in rows:
        inventory.append({
            "brick_type_id": row[4],
            "color_id": row[5],
            "name": row[6],
            "quantity": row[7],
        })

    return {
        "set": set_data,
        "inventory": inventory,
    }


def build_400_response():
    return Response(
        json.dumps({"error": "Missing set id"}, indent=4),
        status=400,
        content_type="application/json"
    )


def build_400_response_binary():
    return Response(
        b"Missing set id",
        status=400,
        content_type="text/plain; charset=utf-8"
    )


def build_404_response():
    return Response(
        json.dumps({"error": "Set not found"}, indent=4),
        status=404,
        content_type="application/json"
    )


def build_404_response_binary():
    return Response(
        b"Set not found",
        status=404,
        content_type="text/plain; charset=utf-8"
    )


def return_cached_data(cached_data):
    return Response(
        json.dumps(cached_data, indent=4),
        content_type="application/json"
    )


def build_set_json(db, set_id, cache=None):
    if not set_id:
        return None, 400

    if cache is not None:
        cached_data = cache.get(set_id)
        if cached_data is not None:
            return json.dumps(cached_data, indent=4), 200

    query, params = get_set_with_inventory(set_id)
    rows = db.fetch_all(query, params)

    data = build_set_response(rows)
    if data is None:
        return None, 404

    if cache is not None:
        cache.put(set_id, data)

    return json.dumps(data, indent=4), 200


def build_sets_page_html(db, template, meta_charset):
    rows = db.fetch_all(get_all_sets())
    rendered_rows = build_rows(rows)
    return replace_placeholders(template, meta_charset, rendered_rows)


def build_set_binary_response(db, set_id):
    if not set_id:
        return None, 400

    query, params = get_set_with_inventory(set_id)
    rows = db.fetch_all(query, params)

    data = build_set_response(rows)
    if data is None:
        return None, 404

    return build_kine_bytes(data), 200


def build_sets_response(compressed_html, encoding):
    return Response(
        compressed_html,
        content_type=f"text/html; charset={encoding}",
        headers={
            "Content-Encoding": "gzip",
            "Cache-Control": "public, max-age=60",
        },
    )


def load_template():
    with open("./app/templates/sets.html", "r", encoding="utf-8") as f:
        template = f.read()

    return template
