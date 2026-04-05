"""
Database access helpers for the application.

This module provides a small wrapper around the active DatabaseSession.
It centralizes cursor handling and common query execution patterns so that routes and
other application code do not need to work with cursors directly.
"""

from contextlib import contextmanager


class Database:
    """
    Provide convenience methods for executing SQL within an active database session.

    This class does not open or close database connections itself. Instead, it operates on a
    DatabaseSession object, which is responsible for connection lifecycle and transaction handling.
    """
    def __init__(self, db_session):
        """
        Initialize the database helper with an active database session

        :param db_session: An active DatabaseSession object.
        """
        self.db_session = db_session

    @contextmanager
    def _get_cursor(self):
        """
        Yield a database cursor for the current session connection.

        The cursor is automatically closed when the context manager exits.

        :yield: A psycopg cursor bound to the active database session.
        """
        with self.db_session.connection.cursor() as cursor:
            yield cursor

    @contextmanager
    def _execute(self, query, params=None):
        """
        Execute an SQL query and yield the cursor used for execution.

        This helper centralizes the shared pattern of getting a cursor, executing a query, and then
        allowing the caller to decide whether to fetch one row, fetch all rows,
        or complete the statement.

        :param query: The SQL query to execute.
        :param params: Optional query parameters passed to psycopg.
        :return: A psycopg cursor after the query has been executed.
        """

        with self._get_cursor() as cursor:
            cursor.execute(query, params)
            yield cursor

    def execute(self, query, params=None):
        """
        Execute an SQL query that does not need to return rows.

        This method is intended for statements such as INSERT, UPDATE, DELETE or DDL operations
        where no result set needs to be fetched.

        :param query: The SQL query to execute.
        :param params: Optional query parameters passed to psycopg.
        :return: None
        """
        with self._get_cursor() as cursor:
            cursor.execute(query, params)

    def fetch_one(self, query, params=None):
        """
        Execute an SQL query and return a single row.
        If the query returns no rows, psycopg will return None.

        :param query: The SQL query to execute.
        :param params: Optional query parameters passed to psycopg.
        :return: One row from the result set, or None if no row is found.
        """
        with self._execute(query, params) as cursor:
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        """
        Execute an SQL query and return all rows.

        If the query returns no rows, an empty list is returned.

        :param query: The SQL query to execute.
        :param params: Optional query parameters passed to psycopg.
        :return: A list of rows from the result set.
        """
        with self._execute(query, params) as cursor:
            return cursor.fetchall()
