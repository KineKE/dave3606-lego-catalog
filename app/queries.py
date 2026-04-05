"""
Module text goes here.
"""


def get_all_sets():
    return """
           SELECT id, name
           FROM lego_set
           ORDER BY id
           """


def get_one_set(set_id):
    return """
           SELECT id, name
           FROM lego_set
           WHERE id = %s
           """, set_id
