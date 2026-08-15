import pytest

from models import Incident

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db

from uuid import UUID
from fastapi.testclient import TestClient
from app import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

#fixture add
@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

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


    with TestingSessionLocal() as db:
        saved_incident = db.get(Incident, data["incident_id"])

        assert saved_incident is not None
        assert saved_incident.description == data["description"]
        assert saved_incident.production_line == data["production_line"]
        assert saved_incident.status == "created"



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
