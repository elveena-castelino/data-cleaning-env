import copy
from datetime import datetime
from .models import Observation, Action, StepResult
from tasks import load_task
from graders.grader import grade_dataset
from word2number import w2n

MAX_STEPS = 10

class DataCleaningEnv:
    def __init__(self, task_name="easy"):
        task = load_task(task_name)
        self.original_dataset = task["dataset"]
        self.ground_truth = task["ground_truth"]

        self.dataset = None
        self.step_count = 0

    def reset(self):
        self.dataset = copy.deepcopy(self.original_dataset)
        self.step_count = 0
        return self._get_observation()

    def state(self):
        return {
            "remaining_errors": self._count_errors(self.dataset),
            "step_count": self.step_count
        }

    def step(self, action: Action):
        self.step_count += 1
        old_dataset = copy.deepcopy(self.dataset)

        self._apply_action(action)

        errors_before = self._count_errors(old_dataset)
        errors_after = self._count_errors(self.dataset)

        progress = errors_before - errors_after
        reward = 0

        if progress > 0:
            reward += progress * 0.15 + 0.05
        elif progress == 0:
            reward -= 0.05
        else:
            reward -= 0.25

        if errors_after == 0:
            reward += 0.5

        done = errors_after == 0 or self.step_count >= MAX_STEPS

        return StepResult(
            observation=self._get_observation(),
            reward=reward,
            done=done,
            info={"errors_before": errors_before, "errors_after": errors_after}
        )

    def _get_observation(self):
        return Observation(
            dataset=self.dataset,
            step_count=self.step_count,
            remaining_errors=self._count_errors(self.dataset)
        )
        
    def get_score(self):
        return grade_dataset(self.dataset, self.ground_truth)

    def _count_errors(self, dataset):
        errors = 0

        for r, g in zip(dataset, self.ground_truth):
            for k in g:
                if r.get(k) != g.get(k):
                    errors += 1

        if len(dataset) > len(self.ground_truth):
            errors += (len(dataset) - len(self.ground_truth)) * len(self.ground_truth[0])

        if len(dataset) < len(self.ground_truth):
            errors += (len(self.ground_truth) - len(dataset)) * len(self.ground_truth[0])

        return errors

    def _apply_action(self, action: Action):
        if action.action_type == "fill_missing":
            self._fill_missing(action.column)
        elif action.action_type == "standardize_name":
            self._standardize_name()
        elif action.action_type == "convert_type":
            self._convert_type(action.column)
        elif action.action_type == "fix_date_format":
            self._fix_date()
        elif action.action_type == "remove_duplicates":
            self._remove_duplicates()

    def _fill_missing(self, column):
        if not column:
            return

        values = [r.get(column) for r in self.dataset if r.get(column) is not None]
        if not values:
            return

        fill = max(set(values), key=values.count)

        for r in self.dataset:
            if r.get(column) is None:
                r[column] = fill

    def _standardize_name(self):
        for r in self.dataset:
            name = r.get("name")

            if isinstance(name, str):
                name = " ".join(name.strip().split())
                r["name"] = name.title()

    def _convert_type(self, column):
        for r in self.dataset:
            val = r.get(column)

            if isinstance(val, str):
                val = val.strip()

                if val.isdigit():
                    r[column] = int(val)
                else:
                    try:
                        r[column] = w2n.word_to_num(val)
                    except:
                        pass

    def _fix_date(self):
        formats = [
        "%B %d, %Y",   # March 12, 2024 (already correct)
        "%d/%m/%Y",    # 12/03/2024
        "%d-%m-%y",    # 12-03-24
        "%Y/%m/%d",    # 2024/03/12
        "%Y-%m-%d",    # fallback if exists
        ]

        for r in self.dataset:
            val = r.get("date")

            if not isinstance(val, str):
                continue

            val = val.strip()

            for fmt in formats:
                try:
                    parsed = datetime.strptime(val, fmt)
                    r["date"] = parsed.strftime("%B %d, %Y")  # ALWAYS word format
                    break
                except ValueError:
                    continue

    def _remove_duplicates(self):
        seen = set()
        unique = []

        for r in self.dataset:
            key = tuple(sorted(r.items()))
            if key not in seen:
                seen.add(key)
                unique.append(r)

        self.dataset = unique