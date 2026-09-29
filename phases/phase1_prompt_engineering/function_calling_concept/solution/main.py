"""SOLUTION -- Function Calling Schema."""

GRADE_TOOL_SCHEMA: dict = {
    "type": "function",
    "function": {
        "name": "calculate_grade",
        "description": "Calculate the weighted average grade from scores and weights.",
        "parameters": {
            "type": "object",
            "properties": {
                "scores": {"type": "array", "items": {"type": "number"}},
                "weights": {"type": "array", "items": {"type": "number"}},
            },
            "required": ["scores", "weights"],
        },
    },
}


if __name__ == "__main__":
    print(GRADE_TOOL_SCHEMA)
