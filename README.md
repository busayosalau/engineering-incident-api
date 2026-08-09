# Engineering Incident API

A FastAPI service for submitting and validating engineering incident reports.

## Current Features

- `POST /incidents` endpoint
- Pydantic request validation
- Required incident description and production line
- Automated tests for valid and invalid requests

## Setup

Create and activate a Python 3.12 environment, then install dependencies:

```bash
python -m pip install -r requirements.txt

## Run

```bash
uvicorn app:app --reload
