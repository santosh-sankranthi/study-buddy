"""SOLUTION -- Tool Schema Shape: calculate_grade."""
GRADE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate_grade",
        "description": "Calculate weighted average grade from a list of scores and weights.",
        "parameters": {
            "type": "object",
            "properties": {
                "scores": {"type": "array", "items": {"type": "number"}, "description": "Numeric scores"},
                "weights": {"type": "array", "items": {"type": "number"}, "description": "Weights for scores"},
            },
            "required": ["scores", "weights"],
        },
    },
}

if __name__ == "__main__":
    print(GRADE_TOOL_SCHEMA)
