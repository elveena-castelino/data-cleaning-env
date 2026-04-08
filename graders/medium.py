from tasks.medium import get_medium_task
from graders.grader import grade_dataset

def grade_medium():
    task = get_medium_task()
    predicted = task["dataset"]
    ground_truth = task["ground_truth"]
    return grade_dataset(predicted, ground_truth)
