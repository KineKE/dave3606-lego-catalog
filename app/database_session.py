"""
Database session management for the application.

This module provides a context manager that opens a PostgreSQL connection, validates required
environment variables, and ensures the connection is committed/rolled back and closed appropriately.

As a result, this session defines the transaction boundary for the application code that uses it.
"""

import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    """
    Manage the lifecycle of a PostgreSQL database session.

    The context manager opens a connection on entry and ensures that the current transaction
    is either committed on success or rolled back on failure before the connection is closed.
    """

    def __init__(self):
        self._host = os.getenv("DB_HOST")
        self._port = os.getenv("DB_PORT")
        self._name = os.getenv("POSTGRES_DB")
        self._user = os.getenv("POSTGRES_USER")
        self._password = os.getenv("POSTGRES_PASSWORD")
        self._connection = None
        self._validate_config()

    @property
    def is_active(self):
        return self._connection is not None

    @property
    def connection(self):
        if not self.is_active:
            raise RuntimeError(
                "DatabaseSession has no active connection. "
                "Use 'with DatabaseSession() as session:' before accessing the connection."
            )
        return self._connection

    def _validate_config(self):
        """
        Validate that all the required database environment variables are present and valid.
        """
        required_values = {
            "DB_HOST": self._host,
            "DB_PORT": self._port,
            "POSTGRES_DB": self._name,
            "POSTGRES_USER": self._user,
            "POSTGRES_PASSWORD": self._password,
        }

        missing = [key for key, value in required_values.items() if not value]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        try:
            self._port = int(self._port)
        except ValueError:
            raise ValueError(f"Port number must be an integer. {self._port} is not an integer.")

    def __repr__(self):
        return (
            f"DatabaseSession(host={self._host!r}, port={self._port!r}, "
            f"dbname={self._name!r}, connected={self.is_active})"
        )

    def __enter__(self):
        """
        Open a database connection and return the active session object (self).

        :return: DatabaseSession
        """
        self._connection = psycopg.connect(
            host=self._host,
            port=self._port,
            dbname=self._name,
            user=self._user,
            password=self._password)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Commit on success, roll back on failure, and always close the connection.
        """
        if self._connection is None:
            return

        try:
            if exc_type is None:
                self._connection.commit()
            else:
                self._connection.rollback()
        finally:
            self._connection.close()
            self._connection = None
