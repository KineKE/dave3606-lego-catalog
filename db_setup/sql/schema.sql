-- Reset existing tables so the script can be rerun cleanly.
DROP TABLE IF EXISTS lego_inventory;
DROP TABLE IF EXISTS lego_brick;
DROP TABLE IF EXISTS lego_set;

-- =========================================================
-- Table definitions
-- =========================================================

CREATE TABLE lego_set (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    year INT NULL,
    category TEXT NULL,
    preview_image_url TEXT NULL
);

CREATE TABLE lego_brick (
    brick_type_id TEXT NOT NULL,
    color_id INT NOT NULL,
    name TEXT NOT NULL,
    preview_image_url TEXT NULL,
    CONSTRAINT pk_lego_brick PRIMARY KEY (brick_type_id, color_id)
);

CREATE TABLE lego_inventory (
    set_id TEXT NOT NULL,
    brick_type_id TEXT NOT NULL,
    color_id INT NOT NULL,
    count INT NOT NULL,
    CONSTRAINT pk_lego_inventory PRIMARY KEY (set_id, brick_type_id, color_id),
    CONSTRAINT fk_lego_inventory_set
        FOREIGN KEY (set_id)
        REFERENCES lego_set(id),
    CONSTRAINT fk_lego_inventory_brick
        FOREIGN KEY (brick_type_id, color_id)
        REFERENCES lego_brick(brick_type_id, color_id)
);

-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX bricktype_idx
    ON lego_inventory (brick_type_id, set_id);

CREATE INDEX colorid_idx
    ON lego_inventory (color_id, set_id);