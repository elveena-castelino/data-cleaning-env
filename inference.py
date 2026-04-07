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

    try:
        data = json.loads(text)
        return Action(**data)
    except Exception:
        return Action(action_type="standardize_name")


def run_baseline(task):
    env = DataCleaningEnv(task)
    obs = env.reset()

    actions = [
        Action(action_type="standardize_name"),
        Action(action_type="convert_type", column="age"),
        Action(action_type="fill_missing", column="age"),
        Action(action_type="fix_date_format"),
        Action(action_type="remove_duplicates"),
    ]

    total_reward = 0.0
    steps_taken = 0
    result = None

    for step in range(1, MAX_STEPS + 1):
        best_action = None
        best_reward = -float("inf")

        for action in actions:
            test_env = DataCleaningEnv(task)
            test_env.dataset = [row.copy() for row in env.dataset]
            test_result = test_env.step(action)

            if test_result.reward > best_reward:
                best_reward = test_result.reward
                best_action = action

        result = env.step(best_action)

        reward = float(result.reward)
        total_reward += reward
        steps_taken += 1

        print(f"[STEP] step={step} reward={reward}", flush=True)

        if result.done:
            break

    final_errors = int(result.observation.remaining_errors) if result else 0
    success = final_errors == 0

    return total_reward, steps_taken, success


def main():
    tasks = ["easy", "medium", "hard"]

    grand_total_reward = 0.0
    total_steps = 0
    success_count = 0

    print("[START] task=data_cleaning", flush=True)

    for task in tasks:
        total_reward, steps_taken, success = run_baseline(task)

        grand_total_reward += total_reward
        total_steps += steps_taken
        success_count += 1 if success else 0

    avg_score = success_count / len(tasks)

    print(
        f"[END] task=data_cleaning score={avg_score} steps={total_steps}",
        flush=True
    )

if __name__ == "__main__":
    main()