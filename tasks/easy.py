from env.dataset import load_task_dataset

def get_easy_task():
    d, g = load_task_dataset("easy")
    return {"dataset": d, "ground_truth": g}