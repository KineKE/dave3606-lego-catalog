from app.database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE lego_set(
        id TEXT NOT NULL,
        name TEXT NOT NULL ,
        year INT NULL,
        category TEXT NULL,
        preview_image_url TEXT NULL
    );
    """
)
cur.execute(
    """
    CREATE TABLE lego_brick(
        brick_type_id TEXT NOT NULL,
        color_id INT NOT NULL,
        name TEXT NOT NULL,
        preview_image_url TEXT NULL
    );
    """
)
cur.execute(
    """
    CREATE TABLE lego_inventory(
        set_id TEXT NOT NULL,
        brick_type_id TEXT NOT NULL,
        color_id INT NOT NULL,
        count INT NOT NULL
    );
    """
)
cur.close()
conn.commit()
conn.close()
