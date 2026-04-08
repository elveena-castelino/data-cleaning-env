from tasks.hard import get_hard_task
from graders.grader import grade_dataset

def grade_hard():
    task = get_hard_task()
    predicted = task["dataset"]
    ground_truth = task["ground_truth"]
    return grade_dataset(predicted, ground_truth)
