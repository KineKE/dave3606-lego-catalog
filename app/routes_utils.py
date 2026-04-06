import html


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
