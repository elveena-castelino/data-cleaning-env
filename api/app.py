from fastapi import FastAPI, Query
from typing import Optional

from env.environment import DataCleaningEnv
from env.models import Action
from tasks import load_task

app = FastAPI()

# Global state
env = None
task_data = None

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Data Cleaning Environment API",
        "endpoints": [
            "/reset",
            "/step",
            "/state",
            "/tasks",
            "/grader",
            "/baseline",
            "/docs"
        ]
    }

@app.post("/reset")
def reset(payload: Optional[dict] = None, task: Optional[str] = Query(None)):
    global env, task_data

    task_name = task or (payload.get("task") if payload else "easy")

    env = DataCleaningEnv(task_name)

    task_data = None

    return {
        "status": "reset",
        "task": task_name
    }

@app.post("/step")
def step(action: Action):
    global env, task_data

    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}

    if task_data is None:
        task_data = load_task(env.task_name)

    return env.step(action)

@app.get("/state")
def get_state():
    global env

    if env is None:
        return {"error": "Environment not initialized."}

    return env.get_state()

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": ["easy", "medium", "hard"]
    }
    
@app.get("/grader")
def grader():
    return {"status": "grader endpoint ready"}

@app.get("/baseline")
def baseline():
    return {"status": "baseline ready"}