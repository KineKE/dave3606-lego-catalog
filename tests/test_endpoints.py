import gzip

from app.queries import get_all_sets, get_set_with_inventory


def test_index_returns_html(client):
    response = client.get("/")

    assert response.status_code == 200


def test_lego_set_returns_html(client):
    response = client.get("/set")

    assert response.status_code == 200


def test_sets_returns_html_from_database_rows(client, mocked_database):
    mocked_database.fetch_all.return_value = [
        ("10290-1", "Pickup Truck"),
        ("10312-1", "Jazz Club"),
    ]

    response = client.get("/sets")

    mocked_database.fetch_all.assert_called_once_with(get_all_sets())

    html = gzip.decompress(response.data)

    assert response.status_code == 200
    assert b"10290-1" in html
    assert b"Pickup Truck" in html
    assert b"10312-1" in html
    assert b"Jazz Club" in html


def test_api_set_returns_json_from_database_rows(client, mocked_database):
    set_id = "10316-1"
    query, params = get_set_with_inventory(set_id)

    mocked_database.fetch_all.return_value = [
        ("10316-1", "Rivendell", 2023, "Icons", "3001", 1, "Brick 2 x 4", 12),
        ("10316-1", "Rivendell", 2023, "Icons", "3020", 5, "Plate 2 x 4", 3),
    ]

    response = client.get(f"/api/set?id={set_id}")

    mocked_database.fetch_all.assert_called_once_with(query, params)

    assert response.status_code == 200
    assert response.get_json() == {
        "set": {
            "id": "10316-1",
            "name": "Rivendell",
            "year": 2023,
            "category": "Icons",
        },
        "inventory": [
            {
                "brick_type_id": "3001",
                "color_id": 1,
                "name": "Brick 2 x 4",
                "quantity": 12,
            },
            {
                "brick_type_id": "3020",
                "color_id": 5,
                "name": "Plate 2 x 4",
                "quantity": 3,
            },
        ],
    }


def test_api_set_binary_returns_file_from_database_rows(client, mocked_database):
    set_id = "10316-1"
    query, params = get_set_with_inventory(set_id)

    mocked_database.fetch_all.return_value = [
        ("10316-1", "Rivendell", 2023, "Icons", "3001", 1, "Brick 2 x 4", 12),
    ]

    response = client.get(f"/api/set-binary?id={set_id}")

    mocked_database.fetch_all.assert_called_once_with(query, params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.headers["Content-Disposition"] == 'attachment; filename="10316-1.kine"'
    assert response.data != b""