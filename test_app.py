from uuid import UUID
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)



def test_create_incident():
    response = client.post(
        "/incidents",
        json={
            "description": "Hydraulic pressure dropped below specification.",
            "production_line": "Line-3"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "incident_id" in data

    parsed_id = UUID(data["incident_id"])
    assert str(parsed_id) == data["incident_id"]

    assert data["description"] == "Hydraulic pressure dropped below specification."
    assert data["production_line"] == "Line-3"
    assert data["status"] == "created"


def test_missing_description():
    response = client.post(
        "/incidents",
        json={
            "production_line": "Line-3"
        }
    )
    assert response.status_code == 422


def test_empty_description():
    response = client.post(
        "/incidents",
        json={
            "description": "",
            "production_line": "Line-3"
	}
    )
    assert response.status_code == 422


def test_empty_production_line():
    response = client.post(
        "/incidents",
        json={
            "description": " Hydraulic pressure drop below specification.",
            "production_line": ""
        }
    )
    assert response.status_code == 422



def test_incidents_receive_unique_ids():
    incident = {
        "description": "Hydraulic pressure dropped below specification.",
        "production_line": "Line-3"
    }

    first_response = client.post("/incidents", json=incident)
    second_response = client.post("/incidents", json=incident)

    first_id = first_response.json()["incident_id"]
    second_id = second_response.json()["incident_id"]

    assert first_id != second_id
