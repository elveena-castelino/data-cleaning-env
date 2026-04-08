from datetime import datetime

def normalize_date(date_str):
    formats = ["%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y"]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None

def grade_dataset(predicted, ground_truth):
    if len(predicted) != len(ground_truth):
        return 0.01

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

    raw_score = correct / total if total else 0.0
    return 0.01 + (0.98 * raw_score)