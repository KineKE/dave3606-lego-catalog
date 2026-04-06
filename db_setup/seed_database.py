"""
Seed the PostgreSQL database with LEGO data from the Bricklink export.

This script loads the compressed JSON seed file, extracts LEGO sets, unique bricks, and aggregated
inventory rows, and inserts them into the database using the application's DatabaseSession and
Database abstractions.
"""

import gzip
import json
from collections import defaultdict
from pathlib import Path

from app.database import Database
from app.database_session import DatabaseSession


SEED_FILE = Path(__file__).parent / "db_seed_bricklink.json.gz"

def load_seed_data():
    """
    Load and return the LEGO seed data from the compressed JSON seed file.

    :return: A list of LEGO set dictionaries
    """
    with gzip.open(SEED_FILE, "rt", encoding="utf-8") as seed_file:
        return json.load(seed_file)