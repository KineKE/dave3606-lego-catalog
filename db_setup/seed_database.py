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


def collect_unique_bricks(seed_data):
    """
    Collect the unique bricks rows from the LEGO seed data from the Bricklink export.

    Bricks are uniquely identified by the composite key (brick_type_id, color_id). This function
    also validates each such key map to a single consistent name and preview image URL.

    :param seed_data: A list of LEGO set dictionaries
    :return: A dictionary mapping (brick_type_id, color_id) to (name, preview_image_url)
    """

    bricks = defaultdict(seed_data)

    for lego_set in seed_data:
        inventory = lego_set.get("inventory") or []

        for inventory_item in inventory:
            brick_key = (
                inventory_item["brickId"],
                inventory_item["colorId"],
            )
            brick_value = (
                inventory_item["name"],
                inventory_item["previewImageUrl"],
            )
            bricks[brick_key].add(brick_value)

    unique_bricks = {}

    for brick_key, names_and_urls in bricks.items():
        if len(names_and_urls) != 1:
            raise ValueError(
                f"Incorrect brick definition for {brick_key}: {names_and_urls}"
            )

        unique_bricks[brick_key] = next(iter(names_and_urls))

    return unique_bricks


def collect_inventory_rows(seed_data):
    """
    Aggregate inventory rows to match the lego_inventory table structure.

    The raw seed data may contain repeated brick/color combinations within a single set.
    Since lego_inventory uses (set_id, brick_type_id, color_id) as its primary key, those rows
    must be merged and their counts summed before insertion.

    :param seed_data: A list of LEGO set dictionaries.
    :return: A list of tuples in the form (set_id, brick_type_id, color_id, count).
    """

    inventory_rows = []

    for lego_set in seed_data:
        set_id = lego_set["setNumber"]
        inventory = lego_set.get("inventory") or []

        inventory_counts = defaultdict(int)

        for inventory_item in inventory:
            brick_key = (
                inventory_item["brickId"],
                inventory_item["colorId"]
            )
            inventory_counts[brick_key] += inventory_item["count"]

        for (brick_type_id, color_id), count in inventory_counts.items():
            inventory_rows.append((set_id, brick_type_id, color_id, count))

    return inventory_rows


def insert_sets(db, seed_data):
    """
    Insert Lego sets into lego_set.

    :param db: A Database instance.
    :param seed_data: A list of Lego set dictionaries.
    :return: None
    """

    query = """
            INSERT INTO lego_set (id, name, year, category, preview_image_url)
            VALUES (%s, %s, %s, %s, %s)
            """

    for lego_set in seed_data:
        year = lego_set["year"]

        db.execute(
            query,
            (
                lego_set["setNumber"],
                lego_set["name"],
                None if year == 0 else year,
                lego_set["category"],
                lego_set["previewImageUrl"],
            ),
        )


def insert_bricks(db, bricks):
    """
    Insert unique bricks into lego_brick.

    :param db: A Database instance.
    :param bricks: A dictionary mapping (brick_type_id, color_id) to (name, preview_image_url).
    :return: None
    """

    query = """
            INSERT INTO lego_brick (brick_type_id, color_id, name, preview_image_url)
            VALUES (%s, %s, %s, %s)
            """

    for (brick_type_id, color_id), (name, preview_image_url) in bricks.items():
        db.execute(
            query,
            (brick_type_id, color_id, name, preview_image_url),
        )


def insert_inventory(db, inventory_rows):
    """
    Insert aggregated inventory rows into lego_inventory.

    :param db: A Database instance.
    :param inventory_rows: A list of tuples in the form (set_id, brick_type_id, color_id, count).

    :return: None
    """

    query = """
            INSERT INTO lego_inventory (set_id, brick_type_id, color_id, count)
            VALUES (%s, %s, %s, %s)
            """

    for set_id, brick_type_id, color_id, count in inventory_rows:
        db.execute(
            query,
            (set_id, brick_type_id, color_id, count),
        )


def main():
    """
    Seed the database with Lego data.

    :return: None
    """

    sets = load_seed_data()
    bricks = collect_unique_bricks(sets)
    inventory_rows = collect_inventory_rows(sets)

    with DatabaseSession() as session:
        db = Database(session)

        insert_sets(db, sets)
        insert_bricks(db, bricks)
        insert_inventory(db, inventory_rows)

    print("Database seeding completed successfully.")


if __name__ == "__main__":
    main()
