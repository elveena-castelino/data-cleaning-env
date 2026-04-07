from env.dataset import load_task_dataset

def get_medium_task():
    d, g = load_task_dataset("medium")
    return {"dataset": d, "ground_truth": g}