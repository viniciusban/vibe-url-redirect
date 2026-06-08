import json
import logging


def test_create_route_happy_path(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "My Route",
            "destination_url": "https://example.com",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 200
    assert response.json() == {"alias": "my-route"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "alias": "my-route",
        "error_code": 0,
    }


def test_create_route_duplicate(client, caplog):
    client.post("/routes/", json={
        "name": "My Route",
        "destination_url": "https://example.com",
        "expiration": "2027-01-01 00:00:00",
    })

    caplog.clear()

    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "my-route",
            "destination_url": "https://example2.com",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {
        "error_code": 1, "reason": "already exists", "alias": "my-route"
    }

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "alias": "my-route",
        "error_code": 1,
        "reason": "already exists",
    }


def test_create_route_invalid_expiration(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "My Route",
            "destination_url": "https://example.com",
            "expiration": "invalid entry",
        })

    assert response.status_code == 400
    assert response.json() == {
        "error_code": 4, "reason": "invalid expiration", "alias": "my-route"
    }

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "alias": "my-route",
        "error_code": 4,
        "reason": "invalid expiration",
    }
