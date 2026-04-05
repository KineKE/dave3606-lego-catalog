import pytest

# ------------------ DATABASE SESSION CONFIG ------------------------

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
def test_database_session_valid_envs_loads_correctly(session_configured, attribute_name, expected_value):
    """Env variables from .env files should be instantiated as attributes in DatabaseSession.
        The values that are being tested are mocked in conftest.py"""
    assert getattr(session_configured, attribute_name) == expected_value






# ------------------ CONTEXT MANAGER LIFECYCLE ------------------------



# ------------------ INTEGRATION BEHAVIOR --------------------------
