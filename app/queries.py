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


def get_set_with_inventory(set_id):
    query = """
            SELECT s.id,
                   s.name,
                   s.year,
                   s.category,
                   i.brick_type_id,
                   i.color_id,
                   b.name,
                   i.count
            FROM lego_set AS s
                     JOIN lego_inventory AS i
                          ON s.id = i.set_id
                     JOIN lego_brick AS b
                          ON i.brick_type_id = b.brick_type_id
                              AND i.color_id = b.color_id
            WHERE s.id = %s
            ORDER BY b.name
            """

    params = (set_id,)

    return query, params
