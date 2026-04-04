"""
Module text goes here.
"""

import os
import psycopg
from dotenv import load_dotenv
from contextlib import contextmanager

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
        self._validate_config()

    def _validate_config(self):
        required_values = {
            "DB_HOST": self.host,
            "DB_PORT": self.port,
            "POSTGRES_DB": self.name,
            "POSTGRES_USER": self.user,
            "POSTGRES_PASSWORD": self.password,
        }

        missing = [key for key, value in required_values.items() if not value]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)} are required")

    def __repr__(self):
        return f"Database {self.host, self.port, self.name, self.connection, self.cursor}"

    def __enter__(self):
        """
        Set up and require a database connection with psycopg.
        :return: An instance of psycopg.connection
        """
        self.connection = psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.name,
            user=self.user,
            password=self.password)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Shuts down and releases the psycopg.connection, even if an error is raised.
        Transaction!

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.connection.close()

    @contextmanager
    def get_cursor(self):
        pass

    def execute(self, query):
        pass

    def fetch_one(self):
        pass

    def fetch_all(self):
        pass

