"""SOLUTION -- Structured Output."""

from pydantic import BaseModel


class StudyPlanDay(BaseModel):
    subject: str
    topics: list[str]
    minutes: int


def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    """Validate each dict and return the list of StudyPlanDay."""
    return [StudyPlanDay.model_validate(item) for item in json_list]


if __name__ == "__main__":
    print(parse_and_validate_plan([{"subject": "Math", "topics": ["Algebra"], "minutes": 60}]))
