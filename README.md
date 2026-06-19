# DevOps Todo

A small FastAPI todo service used as a vehicle to learn DevOps end to end:
version control, containers, CI/CD, infrastructure as code, Kubernetes, and monitoring.

## Run locally

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs

## Test

    pytest
