from fastapi import FastAPI

app = FastAPI()

# Global env
env = None


# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def home():
    return {"status": "running"}


# ----------------------------
# RESET (VERY FAST ⚡)
# ----------------------------
@app.post("/reset")
def reset():
    global env

    # Lazy import (only when needed)
    from env.environment import DataCleaningEnv

    env = DataCleaningEnv("easy")

    return {"status": "ok"}


# ----------------------------
# STEP
# ----------------------------
@app.post("/step")
def step(action: dict):
    global env

    if env is None:
        return {"error": "Call /reset first"}

    from env.models import Action

    action_obj = Action(**action)

    return env.step(action_obj)


# ----------------------------
# STATE
# ----------------------------
@app.get("/state")
def state():
    global env

    if env is None:
        return {"error": "Call /reset first"}

    return env.state()


# ----------------------------
# TASKS
# ----------------------------
@app.get("/tasks")
def tasks():
    return {"tasks": ["easy", "medium", "hard"]}