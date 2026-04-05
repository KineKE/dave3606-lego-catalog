import pytest
from unittest.mock import patch

from app.database_session import DatabaseSession


@pytest.mark.parametrize(
    "attribute_name, expected_value",
    [
        ("_host", "localhost"),
        ("_port", 9876),
        ("_name", "lego-db"),
        ("_user", "lego"),
        ("_password", "bricks")
    ],
)
def test_database_session_valid_envs_load_correctly(session_configured, attribute_name, expected_value):
    """
    DatabaseSession should load and normalize the expected environment variables.
    The port is expected to be converted from string to integer during validation.
    """
    assert getattr(session_configured, attribute_name) == expected_value


def test_session_connection_is_inactive_before_enter(session_configured):
    """
    A DatabaseSession should not be active (have a connection) before entering the context manager.
    """
    assert session_configured._connection is None


def test_database_session_connection_raises_when_inactive(session_configured):
    """
    Accessing the public connection property before entering the context manager should
    raise a RuntimeError.
    """
    with pytest.raises(RuntimeError, match="no active connection"):
        _ = session_configured.connection


def test_database_session_opens_connection_when_entered(fake_active_session, fake_connection, connect_patched):
    """
    Entering the context manager should open a psycopg connection using the validated
    environment value.
    """
    assert fake_active_session.is_active is True
    assert fake_active_session.connection is fake_connection

    connect_patched.assert_called_once_with(
        host="localhost",
        port=9876,
        dbname="lego-db",
        user="lego",
        password="bricks",
    )


def test_database_session_commits_on_success(fake_env, fake_connection):
    """
    On normal exit, the session should commit and close the connection.
    """
    with patch("app.database_session.psycopg.connect", return_value=fake_connection):
        with DatabaseSession():
            pass

        fake_connection.commit.assert_called_once()
        fake_connection.rollback.assert_not_called()
        fake_connection.close.assert_called_once()


def test_database_session_rolls_back_on_exception(fake_env, fake_connection):
    """
    If an exception happens inside the context manager, the session should roll back and still
    close the connection.
    """
    with patch("app.database_session.psycopg.connect", return_value=fake_connection):
        with pytest.raises(ValueError, match="errorohno"):
            with DatabaseSession():
                raise ValueError("errorohno")

    fake_connection.rollback.assert_called_once()
    fake_connection.commit.assert_not_called()
    fake_connection.close.assert_called_once()


def test_database_session_is_inactive_after_exit(fake_env, fake_connection):
    """
    After leaving the context manager, the session should no longer be active.
    """
    with patch("app.database_session.psycopg.connect", return_value=fake_connection):
        with DatabaseSession() as session:
            pass

    assert session.is_active is False


@pytest.mark.parametrize(
    "missing_key",
    [
        "DB_HOST",
        "DB_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ],
)
def test_database_session_raises_for_missing_env_vars(fake_env, monkeypatch, missing_key):
    """
    Missing required environment variables should raise a RuntimeError.
    """
    monkeypatch.delenv(missing_key, raising=False)

    with pytest.raises(ValueError, match="Missing required environment variables"):
        DatabaseSession()


def test_database_session_raises_for_non_integer_port(fake_env, monkeypatch):
    """
    A non-integer DB_PORT should raise a ValueError.
    """
    monkeypatch.setenv("DB_PORT", "thisisnotanumbertehe")

    with pytest.raises(ValueError, match="Port number must be an integer"):
        DatabaseSession()
