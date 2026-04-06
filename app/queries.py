"""
Module text goes here.
"""


def get_all_sets():
    query = """
            SELECT id, name
            FROM lego_set
            ORDER BY id
            """

    return query


def get_one_set(set_id):
    query = """
           SELECT id, name
           FROM lego_set
           WHERE id = %s
           """

    params = (set_id,)

    return query, params
