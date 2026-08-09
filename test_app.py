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

    assert response.status_code == 200

    data = response.json()

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
