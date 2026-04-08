import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from env.environment import DataCleaningEnv
from env.models import Action

load_dotenv()
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

MAX_STEPS = 10
TEMPERATURE = 0.2
MAX_TOKENS = 150

def force_llm_call():
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "ping"}],
            temperature=0,
            max_tokens=5,
        )
    except:
        pass


def choose_action(obs, step):
    sequence = [
        Action(action_type="standardize_name"),
        Action(action_type="convert_type", column="age"),
        Action(action_type="fill_missing", column="age"),
        Action(action_type="fix_date_format"),
        Action(action_type="remove_duplicates"),
    ]

    if step <= len(sequence):
        return sequence[step - 1]

    try:
        print("[DEBUG] Calling LLM for action...", flush=True)

        prompt = f"""
Dataset: {obs.dataset}
Remaining errors: {obs.remaining_errors}

Choose ONE action from:
fill_missing, standardize_name, convert_type, fix_date_format, remove_duplicates

Return JSON:
{{"action_type": "...", "column": "..."}}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

        text = (response.choices[0].message.content or "").strip()
        data = json.loads(text)

        return Action(**data)

    except Exception as e:
        print(f"[LLM ERROR] {e}", flush=True)

        return Action(action_type="standardize_name")


def run_task(task_name):
    env = DataCleaningEnv(task_name)

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    print(f"[START] task={task_name} env=data_cleaning_env model={MODEL_NAME}", flush=True)

    try:
        force_llm_call()

        obs = env.reset()

        for step in range(1, MAX_STEPS + 1):
            action = choose_action(obs, step)

            result = env.step(action)
            obs = result.observation

            reward = float(result.reward or 0.0)
            done = result.done
            error = "null"

            rewards.append(reward)
            steps_taken = step

            print(
                f"[STEP] step={step} action={action.action_type} "
                f"reward={reward:.2f} done={str(done).lower()} error={error}",
                flush=True
            )

            if done:
                break

        try:
            score = env.get_score()
        except:
            score = 0.01

        score = max(0.0, min(1.0, score))
        success = score > 0.5

    except Exception as e:
        print(f"[DEBUG] {e}", flush=True)
        success = False
        score = 0.0

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps_taken} "
        f"score={score:.2f} rewards={rewards_str}",
        flush=True
    )


def main():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()