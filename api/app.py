from fastapi import FastAPI
from env.environment import DataCleaningEnv
from env.models import Action
from graders.grader import grade_dataset
from tasks import load_task

app = FastAPI()
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
def reset(task: str = "easy"):
    global env, task_data
    task_data = load_task(task)
    env = DataCleaningEnv(task)
    return env.reset()


@app.post("/step")
def step(action: dict):
    global env, task_data

    if env is None:
        task_data = load_task("easy")
        env = DataCleaningEnv("easy")
        env.reset()

    return env.step(Action(**action))


@app.get("/state")
def state():
    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}
    return env.state()


@app.get("/tasks")
def tasks():
    return {"tasks": ["easy", "medium", "hard"], "action_schema": Action.schema()}


@app.get("/grader")
def grader():
    if env is None or task_data is None:
        return {"error": "Run /reset before grading."}
    return {"score": grade_dataset(env.dataset, task_data["ground_truth"])}


@app.get("/baseline")
def baseline():
    try:
        from inference import run_baseline
        return run_baseline()
    except Exception as e:
        return {"error": str(e)}