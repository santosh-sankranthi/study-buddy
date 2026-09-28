"""EXERCISE -- Structured Output: StudyPlanDay Schema.

The demo validated Flashcard objects.
Your twist: define StudyPlanDay with subject, topics, and minutes,
and validate a list of StudyPlanDay items.

Run when done:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
"""
from pydantic import BaseModel

# TODO(1): Define StudyPlanDay schema
#   subject: str
#   topics: list[str]
#   minutes: int
class StudyPlanDay(BaseModel):
    pass

# TODO(2): Implement parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]
def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    raise NotImplementedError("TODO(2): implement parse_and_validate_plan")

def generate_study_plan(subjects: list[str], total_hours: int) -> list[StudyPlanDay]:
    raise NotImplementedError("TODO: implement generate_study_plan")

if __name__ == "__main__":
    print(generate_study_plan(["Biology", "Math"], 4))
