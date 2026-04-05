import pytest
from app.database_session import DatabaseSession


# Use to mock the .env file
@pytest.fixture
def fake_env(monkeypatch):
    """
    Provides a predictable database environment variables for testing.
    Monkeypatch automatically restores the original environment afterward.
    """
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "9876")
    monkeypatch.setenv("POSTGRES_DB", "lego-db")
    monkeypatch.setenv("POSTGRES_USER", "lego")
    monkeypatch.setenv("POSTGRES_PASSWORD", "bricks")


# Use to test the context manager aspect of the class
# (__new__ + __init__ has been called, but __enter__ has not)
@pytest.fixture
def session_configured(fake_env):
    """
    Return a DatabaseSession instance after env vars have been loaded,
    but before entering the context manager.
    """
    return DatabaseSession()


# Use to test how an instance of the class works, once it has been created as a context manager
# (__enter__ has been called, but not __exit__ yet, so it is the yield that is being tested
@pytest.fixture
def db_session(fake_env):
    """
    Return an open DatabaseSession inside the context manager.
    Teardown happens automatically when the test finishes.
    """
    with DatabaseSession() as session:
        yield session



