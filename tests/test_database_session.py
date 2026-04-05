import pytest


######################
###    FIXTURES    ###
######################




# ------------------ DATABASE SESSION CONFIG ------------------------


def test_database_session_valid_envs_loads_correctly(variable):
    """Env variables from .env files should be instantiated as attributes in DatabaseSession"""
    with DatabaseSession() as session:
        assert session.variable == "localhost"

def test_database_session_missing_requirement_raises_error():
    pass


def test_database_session_invalid_port_raises_error():
    """Env variables from .env files should be instantiated as attributes in DatabaseSession"""
    with DatabaseSession() as session:
        assert session._port == '9876'


# TODO: Test that the env variables are loaded correctly
# TODO: Test that the _port is converted into an int (hm, its not, right now actually, so should change that too)
# TODO: Create a mock environment for psycopg/fixture
# TODO: Create a mock environment for the env variables/fixture


# ------------------ CONTEXT MANAGER LIFECYCLE ------------------------



# ------------------ INTEGRATION BEHAVIOR --------------------------
