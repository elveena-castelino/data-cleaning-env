# inference.py

import os
import requests
from openai import OpenAI
from openai import APIConnectionError
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
    try:
        obs = requests.post(f"{API_URL}/reset", json={"task": task_name}, timeout=10)
        obs.raise_for_status()
        obs = obs.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not reach API at {API_URL}. Start the server before running inference.") from exc

    done = False

    while not done:
        try:
            action = choose_action(obs)
        except APIConnectionError as exc:
            raise RuntimeError("Could not reach the model backend. Check your API key and network access.") from exc

        result = requests.post(f"{API_URL}/step", json=action, timeout=10)
        result.raise_for_status()
        result = result.json()

        done = result["done"]

    score = requests.get(f"{API_URL}/grader", timeout=10)
    score.raise_for_status()
    score = score.json()["score"]
    return score


def run_baseline(task):
    env = DataCleaningEnv(task)
    env.reset()

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
            "reward": float(result.reward),
            "remaining_errors": int(result.observation.remaining_errors)
        })

        if result.done:
            break

    return {
        "final_dataset": env.dataset,
        "steps": history,
        "final_errors": int(result.observation.remaining_errors),
        "success": result.observation.remaining_errors == 0
    }

if __name__ == "__main__":
    print(run_baseline())
