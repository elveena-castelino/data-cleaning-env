from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    return {"status": "reset ok"}