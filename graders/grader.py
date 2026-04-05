from datetime import datetime

def normalize_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
            return None

def grade_dataset(predicted, ground_truth):
    if len(predicted) != len(ground_truth):
        return 0.0

    total, correct = 0, 0

    for p, g in zip(predicted, ground_truth):
        for k in g:
            total += 1

            if k == "date":
                if normalize_date(p.get(k)) == normalize_date(g.get(k)):
                    correct += 1
            else:
                if p.get(k) == g.get(k):
                    correct += 1

    return correct / total if total else 0.0
