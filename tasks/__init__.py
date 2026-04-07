<<<<<<< HEAD
from env.dataset import get_task

def load_task(name):
    if name in ["easy", "medium", "hard"]:
        return get_task(name)
=======
from env.dataset import get_task

def load_task(name):
    if name in ["easy", "medium", "hard"]:
        return get_task(name)
>>>>>>> d4d54a4fbfdb771cbe88107dcf9cd40ac0e2efc2
    raise ValueError("Invalid task")