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
    ALTER TABLE lego_set 
        DROP CONSTRAINT IF EXISTS
            pk_lego_set;
        
    ALTER TABLE lego_set
        ADD CONSTRAINT pk_lego_set
        PRIMARY KEY (id);
    """
)
cur.execute(
    """
    ALTER TABLE lego_brick 
        DROP CONSTRAINT IF EXISTS
        pk_lego_brick;
        
    ALTER TABLE lego_brick
        ADD CONSTRAINT pk_lego_brick
        PRIMARY KEY (brick_type_id, color_id);
    """
)
cur.execute(
    """
    ALTER TABLE lego_inventory 
        DROP CONSTRAINT IF EXISTS
        fk_lego_inventory_set;
        
    ALTER TABLE lego_inventory 
        DROP CONSTRAINT IF EXISTS
        fk_lego_inventory_brick;
        
    ALTER TABLE lego_inventory 
        DROP CONSTRAINT IF EXISTS
        pk_lego_inventory;
        
    ALTER TABLE lego_inventory
        ADD CONSTRAINT pk_lego_inventory
        PRIMARY KEY (set_id, brick_type_id, color_id);
        
    ALTER TABLE lego_inventory
        ADD CONSTRAINT fk_lego_inventory_set
        FOREIGN KEY (set_id)
        REFERENCES lego_set(id);
        
    ALTER TABLE lego_inventory
        ADD CONSTRAINT fk_lego_inventory_brick
        FOREIGN KEY (brick_type_id, color_id)
        REFERENCES lego_brick(brick_type_id, color_id);
    """
)
cur.close()
conn.commit()
conn.close()
