from app.database import Database
from app.database_session import DatabaseSession
from app.queries import get_one_set


def test_get_one_set_against_real_database():
    """
    Integration test for retrieving a single Lego set from the real database.

    This test verifies that DatabaseSession, Database, and the SQL query from
    queries.py work together correctly by fetching one known row from the database.
    """
    with DatabaseSession() as session:
        db = Database(session)
        query, params = get_one_set("10290-1")

        result = db.fetch_one(query, params)

        assert result == ("10290-1", "Pickup Truck")