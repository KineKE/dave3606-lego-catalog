"""
Module text goes here.
"""
import struct


MAGIC = b"KINE"
VERSION = 1


def pack_string(value):
    encoded = value.encode("utf-8")
    return struct.pack(">H", len(encoded)) + encoded


def build_kine_bytes(data):
    """
    Convert a Lego set response structure into the custom .kine binary format.

    Expected input format:
    {
        "set": {
            "id": "...",
            "name": "...",
            "year": 2022,
            "category": "..."
        },
        "inventory": [
            {
                "brick_type_id": "...",
                "color_id": 3,
                "name": "...",
                "quantity": 12
            },
            ...
        ]
    }
    """
    set_data = data["set"]
    inventory = data["inventory"]

    parts = [
        MAGIC,
        struct.pack(">B", VERSION),
        pack_string(set_data["id"]),
        pack_string(set_data["name"]),
        struct.pack(">H", set_data["year"]),
        pack_string(set_data["category"]),
        struct.pack(">I", len(inventory)),
    ]

    for item in inventory:
        parts.append(pack_string(str(item["brick_type_id"])))
        parts.append(pack_string(str(item["color_id"])))
        parts.append(pack_string(item["name"]))
        parts.append(struct.pack(">I", item["quantity"]))

    return b"".join(parts)