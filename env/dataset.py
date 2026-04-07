import copy

def base_clean_dataset():
    return [
        {"name": "John Doe", "age": 25, "date": "March 12, 2024"},
        {"name": "Jane Doe", "age": 25, "date": "March 12, 2024"},
        {"name": "Alice Smith", "age": 22, "date": "March 12, 2024"},
    ]

def introduce_errors(clean_data, level="easy"):
    data = copy.deepcopy(clean_data)

    if level == "easy":
        data[1]["age"] = None

    elif level == "medium":
        data[0]["name"] = "john doe"
        data[1]["age"] = None
        data[2]["date"] = "12/03/2024"

    elif level == "hard":
        data[0]["name"] = "JOHN    DOE"
        data[1]["age"] = " twenty five "
        data[2]["date"] = "12-03-24"

        #messy duplicate with different format
        data.append({
            "name": "alice smith ",
            "age": "22",
            "date": "2024/03/12"
        })

        #logical duplicate
        data.append({
            "name": "John Doe",
            "age": 25,
            "date": "March 12, 2024"
        })

    return data

def load_task_dataset(level):
    clean = base_clean_dataset()
    dirty = introduce_errors(clean, level)
    return dirty, clean

#wrapper for OpenEnv
def get_task(level):
    dirty, clean = load_task_dataset(level)

    return {
        "dataset": dirty,
        "ground_truth": clean
    }