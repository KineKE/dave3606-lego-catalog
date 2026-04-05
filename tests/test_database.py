import pytest
from app.database import Database


def test_database_execution_runs_query_with_params(database, fake_connection, fake_cursor):
    """
    execute() should open a cursor and execute the given query with parameters
    """

    query = "DELETE FROM lego_set WHERE id = %s"
    params = ("123",)

    database.execute(query, params)

    fake_connection.cursor.assert_called_once()
    fake_cursor.execute.assert_called_once_with(query, params)


def test_database_execute_runs_query_without_params(database, fake_cursor):
    """
    execute() should also execute the given query without parameters
    """
    query = "HEIDU"
    database.execute(query)

    fake_cursor.execute.assert_called_once_with(query, None)


def test_database_fetch_one_executes_query_and_returns_row(database, fake_cursor):
    """
    fetch_one() should execute the query and return cursor.fetchone().
    """
    query = "SELECT id, name FROM lego_set WHERE id = %s"
    params = ("10290-1",)
    fake_cursor.fetchone.return_value = ("10290-1", "Pickup Truck")

    result = database.fetch_one(query, params)

    fake_cursor.execute.assert_called_once_with(query, params)
    fake_cursor.fetchone.assert_called_once()
    assert result == ("10290-1", "Pickup Truck")


def test_database_fetch_one_returns_none_when_no_row_found(database, fake_cursor):
    """
    fetch_one() should return None when the query returns no rows.
    """
    query = "SELECT id, name FROM lego_set WHERE id = %s"
    params = ("nothing",)
    fake_cursor.fetchone.return_value = None

    result = database.fetch_one(query, params)

    fake_cursor.execute.assert_called_once_with(query, params)
    fake_cursor.fetchone.assert_called_once()
    assert result is None


def test_database_fetch_all_executes_query_and_returns_rows(database, fake_cursor):
    """
    fetch_all() should execute the query and return cursor.fetchall().
    """
    query = "SELECT id, name FROM lego_set WHERE id = %s"
    fake_cursor.fetchall.return_value = [
        ("10290-1", "Pickup Truck"),
        ("10312-1", "Jazz Club")
    ]

    result = database.fetch_all(query)

    fake_cursor.execute.assert_called_once_with(query, None)
    fake_cursor.fetchall.assert_called_once()
    assert result == [
        ("10290-1", "Pickup Truck"),
        ("10312-1", "Jazz Club")
    ]


def test_database_fetch_all_returns_empty_list_when_no_rows(database, fake_cursor):
    """
    fetch_all() should return an empty list when the query returns no rows.
    """
    query = "SELECT id FROM lego_set WHERE year = %s"
    params = (1800,)
    fake_cursor.fetchall.return_value = []

    result = database.fetch_all(query, params)

    fake_cursor.execute.assert_called_once_with(query, params)
    fake_cursor.fetchall.assert_called_once()
    assert result == []


def test_database_raises_exception_if_session_is_not_active(session_configured):
    """
    Database should fail when used with a session that has not entered the context manager.
    """
    db = Database(session_configured)

    with pytest.raises(RuntimeError):
        db.execute("SELECT 1")
