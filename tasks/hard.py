from env.dataset import load_task_dataset

def get_hard_task():
    d, g = load_task_dataset("hard")
    return {"dataset": d, "ground_truth": g}