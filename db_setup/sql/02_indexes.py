from app.database import get_connection

conn = get_connection()
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
