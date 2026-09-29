"""EXERCISE -- Tools: register a real function.

Practice: a tool is just a Python function the model may call by name.

Task: finish calculate_grade() and add it to TOOL_REGISTRY.

Check your work with:
    python phases/phase3_agents_and_tools/tools/solution/check.py
"""

SCORES = [80.0, 90.0, 70.0]
WEIGHTS = [0.3, 0.4, 0.3]


def calculate_grade(scores: list[float], weights: list[float]) -> str:
    """Return the weighted average, e.g. 'Weighted average grade: 81.00%'."""
    # TODO: divide sum(score * weight) by sum(weights) and format with :.2f.
    raise NotImplementedError("calculate_grade")


TOOL_REGISTRY: dict[str, object] = {}
# TODO: TOOL_REGISTRY["calculate_grade"] = calculate_grade


if __name__ == "__main__":
    print(calculate_grade(SCORES, WEIGHTS))
    print("Registered tools:", list(TOOL_REGISTRY))
