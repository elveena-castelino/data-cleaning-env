from pydantic import BaseModel
from typing import List, Dict, Optional, Literal


class Observation(BaseModel):
    dataset: List[Dict]
    step_count: int
    remaining_errors: int

class Action(BaseModel):
    action_type: Literal[
        "fill_missing",
        "standardize_name",
        "convert_type",
        "fix_date_format",
        "remove_duplicates"
    ]
    column: Optional[Literal["age"]] = None

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict = {}