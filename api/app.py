from fastapi import FastAPI

app = FastAPI()

env = None


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/reset")
def reset():
    global env

    # import ONLY here
    from env.environment import DataCleaningEnv

    env = DataCleaningEnv("easy")

    return {"status": "ok"}


@app.post("/step")
def step(action: dict):
    global env

    if env is None:
        return {"error": "Call /reset first"}

    from env.models import Action

    return env.step(Action(**action))


@app.get("/state")
def state():
    global env

    if env is None:
        return {"error": "Call /reset first"}

    return env.state()