from fastapi import FastAPI, HTTPException
from env.environment import DataCleaningEnv
from env.models import Action
from graders.grader import grade_dataset
from tasks import load_task

app = FastAPI(title="Data Cleaning Environment API")

env = None
task_data = None

@app.get("/")
def home():
    return {"message": "Data Cleaning API is running"}

@app.post("/reset")
def reset(task: str = "easy"):
    global env, task_data

    if task not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=400, detail="Invalid task")

    task_data = load_task(task)
    env = DataCleaningEnv(task)

    return env.reset()


@app.post("/step")
def step(action: Action):
    global env

    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")

    try:
        return env.step(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    global env

    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")

    return env.state()


@app.get("/tasks")
def tasks():
    return {
        "tasks": ["easy", "medium", "hard"],
        "action_schema": Action.schema()
    }


@app.get("/grader")
def grader():
    global env, task_data

    if env is None or task_data is None:
        raise HTTPException(status_code=400, detail="Environment not initialized.")

    return {
        "score": grade_dataset(env.dataset, task_data["ground_truth"])
    }


@app.get("/baseline")
def baseline(task: str = "easy"):
    from inference import run_baseline

    return run_baseline(task)