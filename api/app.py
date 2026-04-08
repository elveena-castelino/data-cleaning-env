from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Data Cleaning API",
    description="API for OpenEnv validation (reset endpoint + health check)",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "API is running",
        "status": "ok"
    }

@app.post("/reset")
def reset():
    return {
        "status": "ok"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

class StepRequest(BaseModel):
    action_type: str
    column: Optional[str] = None

@app.post("/step")
def step(request: StepRequest):
    """
    Placeholder step endpoint.
    Not required for validation, but useful if you expand later.
    """
    return {
        "received_action": request.action_type,
        "column": request.column,
        "status": "processed"
    }