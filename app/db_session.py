"""
Module text goes here.
"""

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.name = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.connection = None
        self.cursor = None

    def _validate_blabla(self):
        pass

    def __repr__(self):
        return f"Database ('{self.host, self.port, self.name}')"

    def __enter__(self):
        self.connection = psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.name,
            user=self.user,
            password=self.password)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Transaction!

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.connection.close()


    def get_cursor(self):
        pass

    def fetch_all(self):
        pass

    def fetch_one(self):
        pass

    def execute(self, query):
        pass
