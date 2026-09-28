"""SOLUTION -- Structured Output: StudyPlanDay Schema."""
from pydantic import BaseModel

class StudyPlanDay(BaseModel):
    subject: str
    topics: list[str]
    minutes: int

def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    return [StudyPlanDay.model_validate(item) for item in json_list]

def generate_study_plan(subjects: list[str], total_hours: int) -> list[StudyPlanDay]:
    sample = [
        {"subject": s, "topics": [f"{s} Fundamentals", f"{s} Advanced"], "minutes": (total_hours * 60) // len(subjects)}
        for s in subjects
    ]
    return parse_and_validate_plan(sample)

if __name__ == "__main__":
    print(generate_study_plan(["Biology", "Math"], 4))
