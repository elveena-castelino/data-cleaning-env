from datetime import datetime


def normalize_date(date_str):
    formats = ["%B %d, %Y", "%Y-%m-%d"]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue

    return date_str


def grade_dataset(predicted, ground_truth):
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