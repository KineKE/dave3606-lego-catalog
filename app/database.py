"""
Module text goes here.
"""
from contextlib import contextmanager


class Database:
    def __init__(self, db_session):
        self.db_session = db_session

    @contextmanager
    def get_cursor(self):
        pass

    def execute(self, query):
        pass

    def fetch_one(self):
        pass

    def fetch_all(self):
        pass
