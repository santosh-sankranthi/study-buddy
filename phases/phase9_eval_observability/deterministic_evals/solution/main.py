"""SOLUTION -- Deterministic Schema Detail Check."""
def verify_study_plan_topics(plan: list[dict]) -> dict[str, bool]:
    valid_format = all(isinstance(day.get("topics"), list) for day in plan)
    non_empty_lists = all(len(day.get("topics", [])) > 0 for day in plan)
    valid_strings = all(
        all(isinstance(t, str) and len(t.strip()) > 0 for t in day.get("topics", []))
        for day in plan
    )
    return {
        "valid_format": valid_format,
        "non_empty_lists": non_empty_lists,
        "valid_strings": valid_strings,
        "passed": valid_format and non_empty_lists and valid_strings,
    }

if __name__ == "__main__":
    sample = [{"subject": "Math", "topics": ["Algebra", "Calculus"], "minutes": 60}]
    print(verify_study_plan_topics(sample))
