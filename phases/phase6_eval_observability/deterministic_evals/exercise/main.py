"""EXERCISE -- Deterministic Schema Detail Check.

The demo tested Flashcard schema types.
Your twist: implement verify_study_plan_topics(plan: list[dict]) -> dict[str, bool]
to verify that every day has a non-empty list of non-empty strings for topics.

Run when done:
    python phases/phase6_eval_observability/deterministic_evals/solution/check.py
"""
# TODO(1): Implement verify_study_plan_topics(plan: list[dict]) -> dict[str, bool]
def verify_study_plan_topics(plan: list[dict]) -> dict[str, bool]:
    raise NotImplementedError("TODO(1): implement verify_study_plan_topics")

if __name__ == "__main__":
    sample_plan = [{"subject": "Math", "topics": ["Algebra", "Calculus"], "minutes": 60}]
    print(verify_study_plan_topics(sample_plan))
