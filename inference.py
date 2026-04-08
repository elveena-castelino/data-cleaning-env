import os
import json
from openai import OpenAI
from env.models import Action
from env.environment import DataCleaningEnv
from dotenv import load_dotenv

from graders.grader import grade_dataset
from tasks import load_task

load_dotenv()

# ✅ REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-endpoint>")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

MAX_STEPS = 10
TEMPERATURE = 0.2
MAX_TOKENS = 200

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


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


def run_agent(task):
    env = DataCleaningEnv(task)
    obs = env.reset()

    rewards = []
    steps_taken = 0
    result = None

    # ✅ START (per task)
    print(f"[START] task={task} env=data_cleaning_env model={MODEL_NAME}", flush=True)

    try:
        for step in range(1, MAX_STEPS + 1):
            obs_dict = obs.model_dump()

            llm_action = choose_action(obs_dict)
            best_action = get_best_action(env, task, llm_action)

            result = env.step(best_action)
            obs = result.observation

            reward = round(float(result.reward), 2)
            done = result.done
            error = "null"

            rewards.append(reward)
            steps_taken = step
            
            error_val = error if error else "null"
            print(
                f"[STEP] step={step} action={best_action.action_type} "
                f"reward={reward:.2f} done={str(done).lower()} error={error_val}",
                flush=True
            )

            if done:
                break

        final_errors = int(result.observation.remaining_errors) if result else 0
        success = final_errors == 0

        score = grade_dataset(env.dataset, load_task(task)["ground_truth"])
        score = max(0.0, min(1.0, score))

    except Exception as e:
        # ensure END always prints
        success = False
        score = 0.0

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    # ✅ END (per task)
    print(
        f"[END] success={str(success).lower()} steps={steps_taken} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True
    )


def main():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        run_agent(task)


if __name__ == "__main__":
    main()