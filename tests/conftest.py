import pytest
from unittest.mock import MagicMock, patch

from app.database_session import DatabaseSession
from app.database import Database


@pytest.fixture
def fake_env(monkeypatch):
    """
    Provides a predictable database environment variables for testing.
    Monkeypatch automatically restores the original environment afterward.

    This avoids it depending on the developer's real shell environment or .env file.
    """
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "9876")
    monkeypatch.setenv("POSTGRES_DB", "lego-db")
    monkeypatch.setenv("POSTGRES_USER", "lego")
    monkeypatch.setenv("POSTGRES_PASSWORD", "bricks")


@pytest.fixture
def session_configured(fake_env):
    """
    Return a DatabaseSession instance after initialization, but before entering the context manager.

    Use this fixture for testing that verifies:
    - environment variable loading
    - validation behavior
    - inactive session behavior
    """
    return DatabaseSession()


@pytest.fixture
def fake_cursor():
    """
    Return a mock cursor that supports context manager usage.

    This allows Database._get_cursor() to use:
        with connection.cursor() as cursor:
            ...
    """
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = None
    return cursor


@pytest.fixture
def fake_connection(fake_cursor):
    """
    Return a mock database connection.

    The mock supports:
    - cursor()
    - commit()
    - rollback()
    - close()
    """
    connection = MagicMock()
    connection.cursor.return_value = fake_cursor
    return connection


@pytest.fixture
def connect_patched(fake_connection):
    """
    Patch psycopg.connect so DatabaseSession receives a fake connection.
    Yield the mocked connection so tests can assert how it was called.
    """
    with patch("app.database_session.psycopg.connect", return_value=fake_connection) as mock_connect:
        yield mock_connect


@pytest.fixture
def fake_active_session(fake_env, connect_patched):
    """
    Return an active DatabaseSession whose psycopg connection is mocked.

    This fixture is useful when testing code that requires a live session,
    but should not talk to a real PostgreSQL database.
    """
    with DatabaseSession() as session:
        yield session


@pytest.fixture
def database(fake_active_session):
    """
    Return a Database helper bound to an active session with a mocked connection.

    Use this for tests for execute(), fetch_one(), and fetch_all().
    """
    return Database(fake_active_session)
