import html


def build_rows(query_result):

    rows = []
    for row in query_result:
        html_safe_id = html.escape(row[0])
        html_safe_name = html.escape(row[1])

        rows.append(
                f'<tr><td><a href="/set?id={html_safe_id}">{html_safe_id}</a></td><td>{html_safe_name}</td></tr>\n'
            )

    rows = "\n".join(rows)

    return rows
