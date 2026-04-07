import os
import json
from openai import OpenAI, APIConnectionError
from env.models import Action
from env.environment import DataCleaningEnv
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

MAX_STEPS = 10
TEMPERATURE = 0.2
MAX_TOKENS = 200

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def choose_action(observation):
    prompt = f"""
        You are a data cleaning agent.

        Dataset:
        {observation['dataset']}

        Remaining errors: {observation['remaining_errors']}

        Choose ONE best action from:
        fill_missing, standardize_name, convert_type, fix_date_format, remove_duplicates

        Return ONLY valid JSON:
        {{"action_type": "...", "column": "..."}}
        """

    messages = [
        {"role": "system", "content": "You are a precise JSON-only assistant."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        text = response.choices[0].message.content.strip()

    except APIConnectionError:
        return Action(action_type="standardize_name")
    except Exception:
        return Action(action_type="standardize_name")

    # Safe JSON parsing
    try:
        data = json.loads(text)
        return Action(**data)
    except Exception:
        return Action(action_type="standardize_name")


def run_task(task_name):
    env = DataCleaningEnv(task_name)
    obs = env.reset()

    for _ in range(MAX_STEPS):
        action = choose_action(obs.dict())
        result = env.step(action)

        obs = result.observation
        if result.done:
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

    for _ in range(MAX_STEPS):
        best_action = None
        best_reward = -float("inf")

        for action in actions:
            test_env = DataCleaningEnv(task)
            test_env.dataset = [row.copy() for row in env.dataset]
            result = test_env.step(action)

            if result.reward > best_reward:
                best_reward = result.reward
                best_action = action

        result = env.step(best_action)

        history.append({
            "action": best_action.action_type,
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


def main():
    tasks = ["easy", "medium", "hard"]
    results = {}

    for task in tasks:
        results[task] = run_baseline(task)

    avg_score = sum(1 if r["success"] else 0 for r in results.values()) / len(results)

    print("\nDATA CLEANING AGENT RESULTS\n")

    for task, res in results.items():
        print(f"Task: {task.upper()}")
        print(f"--Success: {res['success']}")
        print(f"--Final Errors: {res['final_errors']}")
        print("--Steps:")

        for step in res["steps"]:
            print(f"    > {step['action']} | reward: {step['reward']:.2f} | errors left: {step['remaining_errors']}")

        print()

    print(f"-> Average Score: {avg_score:.2f}")


if __name__ == "__main__":
    main()