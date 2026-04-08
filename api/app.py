from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Global state
env = None
task_data = None


# ----------------------------
# ROOT
# ----------------------------
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


# ----------------------------
# RESET (FAST ⚡)
# ----------------------------
@app.post("/reset")
def reset():
    global env, task_data

    # Lazy import (CRITICAL FIX)
    from env.environment import DataCleaningEnv

    env = DataCleaningEnv("easy")
    task_data = None

    return {"status": "ok"}


# ----------------------------
# STEP
# ----------------------------
@app.post("/step")
def step(action: dict):
    global env, task_data

    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}

    # Lazy imports
    from env.models import Action
    from tasks import load_task

    action_obj = Action(**action)

    if task_data is None:
        task_data = load_task(env.task_name)

    return env.step(action_obj)


# ----------------------------
# STATE
# ----------------------------
@app.get("/state")
def get_state():
    global env

    if env is None:
        return {"error": "Environment not initialized."}

    return env.state()


# ----------------------------
# TASKS
# ----------------------------
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": ["easy", "medium", "hard"]
    }


# ----------------------------
# GRADER
# ----------------------------
@app.get("/grader")
def grader():
    return {"status": "grader endpoint ready"}


# ----------------------------
# BASELINE
# ----------------------------
@app.get("/baseline")
def baseline():
    return {"status": "baseline ready"}