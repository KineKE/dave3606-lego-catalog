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
    """Env variables from .env files should be instantiated as attributes in DatabaseSession.
        The values that are being tested are mocked in conftest.py"""
    assert getattr(session_configured, attribute_name) == expected_value


def test_session_connection_is_inactive_before_enter(session_configured):
    assert session_configured._connection is None


def test_database_session_connection_raises_when_inactive(session_configured):
    with pytest.raises(RuntimeError, match="no active connection"):
        _ = session_configured.connection


def test_database_session_opens_connection_when_entered(fake_env, fake_connection):
    with patch("app.database_session.psycopg.connect", return_value=fake_connection) as mock_connect:
        with DatabaseSession() as session:
            assert session.is_active is True
            assert session.connection is fake_connection

        mock_connect.assert_called_once_with(
            host="localhost",
            port=9876,
            dbname="lego-db",
            user="lego",
            password="bricks",
        )


def test_database_session_commits_on_success(fake_env, fake_connection):
    with patch("app.database_session.psycopg.connect", return_value=fake_connection):
        with DatabaseSession():
            pass

        fake_connection.commit.assert_called_once()
        fake_connection.rollback.assert_not_called()
        fake_connection.close.assert_called_once()


def test_database_session_rolls_back_on_exception(fake_env, fake_connection):
    with patch("app.database_session.psycopg.connect", return_value=fake_connection):
        with pytest.raises(ValueError, match="errorohno"):
            with DatabaseSession():
                raise ValueError("errorohno")

    fake_connection.rollback.assert_called_once()
    fake_connection.commit.assert_not_called()
    fake_connection.close.assert_called_once()


def test_database_session_is_inactive_after_exit(fake_env, fake_connection):
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
    monkeypatch.delenv(missing_key, raising=False)

    with pytest.raises(ValueError, match="Missing required environment variables"):
        DatabaseSession()


def test_database_session_raises_for_non_integer_port(fake_env, monkeypatch):
    monkeypatch.setenv("DB_PORT", "thisisnotanumbertehe")

    with pytest.raises(ValueError, match="Port number must be an integer"):
        DatabaseSession()
