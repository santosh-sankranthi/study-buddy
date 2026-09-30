"""SOLUTION -- Deterministic Schema Check.

Reference answer: validate the plan with plain Python, no API calls.
"""

SAMPLE_PLAN = [
    {"subject": "Math", "topics": ["Algebra", "Calculus"]},
    {"subject": "Biology", "topics": ["Photosynthesis"]},
]


def verify_study_plan_topics(plan: list[dict]) -> bool:
    """Return True if every day has a non-empty list of non-empty strings."""
    for day in plan:
        topics = day.get("topics")
        if not isinstance(topics, list) or not topics:
            return False
        if not all(isinstance(t, str) and t.strip() for t in topics):
            return False
    return True


if __name__ == "__main__":
    print(verify_study_plan_topics(SAMPLE_PLAN))
