"""EXERCISE -- Deterministic Schema Check.

Practice: validate model output with plain Python, no API calls.
Task: finish verify_study_plan_topics() so it returns True only when every day
has a non-empty list of non-empty topic strings.

Check your work with:
    python phases/phase6_eval_observability/deterministic_evals/solution/check.py
"""

SAMPLE_PLAN = [
    {"subject": "Math", "topics": ["Algebra", "Calculus"]},
    {"subject": "Biology", "topics": ["Photosynthesis"]},
]


def verify_study_plan_topics(plan: list[dict]) -> bool:
    """Return True if every day has a non-empty list of non-empty strings."""
    # TODO: check each day's "topics" is a non-empty list of non-empty strings.
    raise NotImplementedError("verify_study_plan_topics")


if __name__ == "__main__":
    print(verify_study_plan_topics(SAMPLE_PLAN))
