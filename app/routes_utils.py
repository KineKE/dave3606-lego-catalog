import html

from flask import Response, json


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


def return_400_missing_set_id():
    return Response(
        json.dumps({"error": "Missing set id"}, indent=4),
        status=400,
        content_type="application/json"
    )


def return_400_missing_set_id_binary():
    return Response(
        b"Missing set id",
        status=400,
        content_type="text/plain; charset=utf-8"
    )


def return_404_set_not_found():
    return Response(
        json.dumps({"error": "Set not found"}, indent=4),
        status=404,
        content_type="application/json"
    )


def return_404_set_not_found_binary():
    return Response(
        b"Set not found",
        status=404,
        content_type="text/plain; charset=utf-8"
    )
