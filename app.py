from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()


class IncidentCreate(BaseModel):
    description: str = Field(min_length=1)
    production_line: str = Field(min_length=1)


@app.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate):
    incident_id = str(uuid4())

    return {
	"incident_id" : incident_id,
        "description": incident.description,
        "production_line": incident.production_line,
        "status": "created"
    }
