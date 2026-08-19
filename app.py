from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Incident


app = FastAPI()
Base.metadata.create_all(bind=engine)


class IncidentCreate(BaseModel):
    description: str = Field(min_length=1)
    production_line: str = Field(min_length=1)


@app.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate,
    db: Session = Depends(get_db)):
    incident_id = str(uuid4())

    db_incident = Incident(
        incident_id=incident_id,
        description=incident.description,
        production_line=incident.production_line,
        status="created"
    )

    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    return {
	"incident_id" : db_incident.incident_id,
        "description": db_incident.description,
        "production_line": db_incident.production_line,
        "status": db_incident.status
    }


@app.get("/incidents/{incident_id}")
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db)
):

    db_incident = db.get(Incident, incident_id)

    if db_incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "incident_id": db_incident.incident_id,
        "description": db_incident.description,
        "production_line": db_incident.production_line,
        "status": db_incident.status
    }
