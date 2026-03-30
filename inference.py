# inference.py

import os
import requests
from openai import OpenAI
from env.models import Action
from env.environment import DataCleaningEnv
from dotenv import load_dotenv
load_dotenv()


API_URL = "http://localhost:8000"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

client = OpenAI(api_key = os.getenv("HF_TOKEN") or os.getenv("API_KEY"))


def choose_action(observation):
    prompt = f"""
    You are a data cleaning agent.

    Dataset:
    {observation['dataset']}

    Remaining errors: {observation['remaining_errors']}

    Choose one action from:
    fill_missing, standardize_name, convert_type, fix_date_format, remove_duplicates

    Return JSON:
    {{"action_type": "...", "column": "..."}}
    """

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    text = response.output_text

    try:
        import json
        return json.loads(text)
    except:
        return {"action_type": "standardize_name"}


def run_task(task_name):
    requests.post(f"{API_URL}/reset?task={task_name}")

    done = False

    while not done:
        obs = requests.get(f"{API_URL}/state").json()

        action = choose_action(obs)
        result = requests.post(f"{API_URL}/step", json=action).json()

        done = result["done"]

    score = requests.get(f"{API_URL}/grader").json()["score"]
    return score


def run_baseline():

    env = DataCleaningEnv("hard")
    obs = env.reset()

    actions = [
        Action(action_type="standardize_name"),
        Action(action_type="convert_type", column="age"),
        Action(action_type="fill_missing", column="age"),
        Action(action_type="fix_date_format"),
        Action(action_type="remove_duplicates"),
    ]

    history = []
    result = None  

    for action in actions:
        result = env.step(action)
        history.append({
            "action": action.action_type,
            "reward": result.reward,
            "remaining_errors": result.observation.remaining_errors
        })

        if result.done:
            break

    return { 
            "final_dataset": env.dataset, 
            "steps": history, 
            "final_errors": int(result.observation.remaining_errors) if result else None, 
            "success": (result.observation.remaining_errors == 0) if result else False 
    }


if __name__ == "__main__":
    print(run_baseline())