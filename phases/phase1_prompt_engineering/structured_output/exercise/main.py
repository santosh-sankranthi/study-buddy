"""EXERCISE -- Structured Output.

Practice: a Pydantic model validates the shape of model output.

Task: fill in StudyPlanDay and parse_and_validate_plan().

Check your work with:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
"""

from pydantic import BaseModel


class StudyPlanDay(BaseModel):
    # TODO(1): fields subject: str, topics: list[str], minutes: int
    pass


def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    """Validate each dict and return the list of StudyPlanDay."""
    # TODO(2): use StudyPlanDay.model_validate() on each item.
    raise NotImplementedError("parse_and_validate_plan")


if __name__ == "__main__":
    print(parse_and_validate_plan([{"subject": "Math", "topics": ["Algebra"], "minutes": 60}]))
