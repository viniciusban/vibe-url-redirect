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
        "error_code": 0,
        "alias": "my-route",
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
    assert response.json() == {"error_code": 1, "reason": "already exists"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 1,
        "reason": "already exists",
    }


def test_create_route_empty_name(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "   ",
            "destination_url": "https://example.com",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 4, "reason": "name is required"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 4,
        "reason": "name is required",
    }


def test_create_route_missing_name(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "destination_url": "https://example.com",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 4, "reason": "name is required"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 4,
        "reason": "name is required",
    }


def test_create_route_name_all_special_chars(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "!@#$%",
            "destination_url": "https://example.com",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 4, "reason": "Invalid name"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 4,
        "reason": "Invalid name",
    }


def test_create_route_empty_destination_url(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "My Route",
            "destination_url": "   ",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 5, "reason": "destination_url is required"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 5,
        "reason": "destination_url is required",
    }


def test_create_route_missing_destination_url(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "My Route",
            "expiration": "2027-01-01 00:00:00",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 5, "reason": "destination_url is required"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 5,
        "reason": "destination_url is required",
    }


def test_create_route_invalid_expiration(client, caplog):
    with caplog.at_level(logging.INFO, logger="steerer"):
        response = client.post("/routes/", json={
            "name": "My Route",
            "destination_url": "https://example.com",
            "expiration": "invalid entry",
        })

    assert response.status_code == 400
    assert response.json() == {"error_code": 4, "reason": "invalid expiration"}

    steerer_records = [r for r in caplog.records if r.name == "steerer"]
    assert len(steerer_records) == 1
    assert json.loads(steerer_records[0].message) == {
        "action": "create route",
        "error_code": 4,
        "reason": "invalid expiration",
    }
