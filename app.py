from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class IncidentCreate(BaseModel):
    description: str
    production_line: str


@app.post("/incidents")
def create_incident(incident: IncidentCreate):
    return {
        "description": incident.description,
        "production_line": incident.production_line,
        "status": "created"
    }
