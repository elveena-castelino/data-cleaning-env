def load_task(name):
    if name not in ["easy", "medium", "hard"]:
        raise ValueError("Invalid task")

    from env.dataset import load_task_dataset

    dataset, ground_truth = load_task_dataset(name)

    return {
        "dataset": dataset,
        "ground_truth": ground_truth,
    }

TASKS = ["easy", "medium", "hard"]