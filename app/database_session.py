"""
Database session management for the application.

This module provides a context manager that opens a PostgreSQL connection, validates required
environment variables, and ensures the connection is committed, rolled back and closed appropriately.
"""

import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    """
    Manage the lifecycle of a PostgreSQL database session.

    The session opens a connection when entering the context manager and ensures that the transaction
    is either committed or rolled back before the connection is closed.
    """

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.name = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.connection = None
        self._validate_config()

    def _validate_config(self):
        """
        Validate that all the required database environment variables are set.
        """
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

        try:
            self.port = int(os.getenv("DB_PORT"))
        except ValueError:
            raise ValueError(f"Port number must be an integer. {self.port} is not an integer.")

    def __repr__(self):
        """
        Return a string representation of the database session.
        """
        return (
            f"DatabaseSession(host={self.host!r}, port={self.port!r}, "
            f"dbname={self.name!r}, connected={self.connection is not None})"
        )

    def __enter__(self):
        """
        Open a database connection and return the session object
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
        Commits on success, rolls back on failure, and always closes the connection.
        """
        if self.connection is None:
            return

        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()
