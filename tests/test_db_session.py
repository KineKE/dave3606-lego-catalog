import pytest

from db_session import DatabaseSession


######################
###    FIXTURES    ###
######################




# ------------------ DATABASE SESSION SET UP ------------------------


def test_database_session_has_correct_env_variables(variable):
    """Env variables from .env files should be instantiated as attributes in DatabaseSession"""
    with DatabaseSession() as session:
        assert session.variable == "localhost"


def test_database_session():
    """Env variables from .env files should be instantiated as attributes in DatabaseSession"""
    with DatabaseSession() as session:
        assert session.port == '9876'


# TODO: Test that the env variables are loaded correctly
# TODO: Test that the port is converted into an int (hm, its not, right now actually, so should change that too)
# TODO: Create a mock environment for psycopg/fixture
# TODO: Create a mock environment for the env variables/fixture



#