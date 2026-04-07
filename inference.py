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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        data = json.loads(text)
        return Action(**data)
    except:
        return Action(action_type="standardize_name")


def run_task(task_name):
    env = DataCleaningEnv(task_name)
    obs = env.reset()

    done = False

    for _ in range(50):
        action = choose_action(obs.dict())
        result = env.step(action)

        obs = result.observation
        done = result.done

        if done:
            break

    return env.get_score()

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
    tasks = ["easy", "medium", "hard"]

    results = {}
    for task in tasks:
        results[task] = run_baseline(task)

    print(results)