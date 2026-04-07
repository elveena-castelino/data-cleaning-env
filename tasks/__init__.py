from env.dataset import get_task

def load_task(name):
    if name in ["easy", "medium", "hard"]:
        return get_task(name)
    raise ValueError("Invalid task")