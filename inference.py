import os
import json
from openai import OpenAI
from env.models import Action
from env.environment import DataCleaningEnv
from dotenv import load_dotenv

from graders.grader import grade_dataset
from tasks import load_task

load_dotenv()

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
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
        {"role": "system", "content": "Return only JSON."},
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
        data = json.loads(text)
        return Action(**data)

    except Exception:
        return Action(action_type="standardize_name")


def get_best_action(env, task, llm_action):
    actions = [
        Action(action_type="standardize_name"),
        Action(action_type="convert_type", column="age"),
        Action(action_type="fill_missing", column="age"),
        Action(action_type="fix_date_format"),
        Action(action_type="remove_duplicates"),
        llm_action,
    ]

    best_action = None
    best_reward = -float("inf")

    for action in actions:
        test_env = DataCleaningEnv(task)
        test_env.dataset = [row.copy() for row in env.dataset]

        result = test_env.step(action)

        if result.reward > best_reward:
            best_reward = result.reward
            best_action = action

    return best_action


def run_agent(task, global_step):
    env = DataCleaningEnv(task)
    obs = env.reset()

    total_reward = 0.0
    steps_taken = 0
    result = None

    for _ in range(MAX_STEPS):
        obs_dict = obs.model_dump()

        llm_action = choose_action(obs_dict)
        best_action = get_best_action(env, task, llm_action)

        result = env.step(best_action)
        obs = result.observation

        reward = round(float(result.reward), 2)

        total_reward += reward
        steps_taken += 1

        print(f"[STEP] step={global_step} reward={reward:.2f}", flush=True)
        global_step += 1

        if result.done:
            break

    final_errors = int(result.observation.remaining_errors) if result else 0
    success = final_errors == 0

    return total_reward, steps_taken, success, env.dataset, global_step


def main():
    tasks = ["easy", "medium", "hard"]

    grand_total_reward = 0.0
    total_steps = 0
    scores = []
    global_step = 1

    print("[START] task=data_cleaning", flush=True)

    for task in tasks:
        task_data = load_task(task)

        total_reward, steps_taken, success, final_dataset, global_step = run_agent(task, global_step)

        score = grade_dataset(final_dataset, task_data["ground_truth"])
        scores.append(score)

        print(f"[TASK] name={task} score={score:.4f}", flush=True)

        grand_total_reward += total_reward
        total_steps += steps_taken

    avg_score = sum(scores) / len(scores)
    avg_score = max(0.01, min(0.99, avg_score))

    print(
        f"[END] task=data_cleaning score={avg_score:.4f} steps={total_steps}",
        flush=True
    )

if __name__ == "__main__":
    main()