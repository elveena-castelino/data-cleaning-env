import uvicorn
from api.app import app

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)