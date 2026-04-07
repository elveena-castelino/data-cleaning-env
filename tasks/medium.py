<<<<<<< HEAD
from env.dataset import load_task_dataset

def get_medium_task():
    d, g = load_task_dataset("medium")
=======
from env.dataset import load_task_dataset

def get_medium_task():
    d, g = load_task_dataset("medium")
>>>>>>> d4d54a4fbfdb771cbe88107dcf9cd40ac0e2efc2
    return {"dataset": d, "ground_truth": g}