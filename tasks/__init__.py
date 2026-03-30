from .easy import get_easy_task
from .medium import get_medium_task
from .hard import get_hard_task

def load_task(name):
    if name == "easy":
        return get_easy_task()
    if name == "medium":
        return get_medium_task()
    if name == "hard":
        return get_hard_task()
    raise ValueError("Invalid task")