"""
Create the PostgreSQL database schema for the lego catalog project.

This script executes the SQL schema file that defines the tables, constraints, and indexes required
by the application.
"""

from pathlib import Path

from app.database import Database
from app.database_session import DatabaseSession

SCHEMA_FILE = Path(__file__).parent / "sql" / "schema.sql"


def load_schema():
    """
    Load and return the SQL
    :return: The contents of the SQL schema file as a string
    """

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        return file.read


def main():
    """
    Build the database schema.
    :return: None
    """

    schema_sql = load_schema()

    with DatabaseSession() as session:
        db = Database(session)
        db.execute(schema_sql)

    print("Database created successfully.")


if __name__ == "__main__":
    main()
