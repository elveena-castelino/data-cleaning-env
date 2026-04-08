from env.dataset import load_task_dataset


def load_task(name):
    if name not in ["easy", "medium", "hard"]:
        raise ValueError("Invalid task")

    dataset, ground_truth = load_task_dataset(name)

    return {
        "dataset": dataset,
        "ground_truth": ground_truth,
    }


# ✅ Explicit task list for validator
TASKS = ["easy", "medium", "hard"]