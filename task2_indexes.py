import psycopg

conn = psycopg.connect(
    host="localhost",
    port=9876,
    dbname="lego-db",
    user="lego",
    password="bricks",
)

cur = conn.cursor()
cur.execute(
    """
    DROP INDEX IF EXISTS bricktype_idx;
        
    CREATE INDEX bricktype_idx
        ON lego_inventory(brick_type_id, set_id);
    """
)
cur.execute(
    """
    DROP INDEX IF EXISTS colorid_idx;

    CREATE INDEX colorid_idx
        ON lego_inventory(color_id, set_id);
    """
)
cur.close()
conn.commit()
conn.close()
