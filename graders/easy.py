from tasks.easy import get_easy_task
from graders.grader import grade_dataset

def grade_easy():
    task = get_easy_task()
    predicted = task["dataset"]
    ground_truth = task["ground_truth"]
    return grade_dataset(predicted, ground_truth)
