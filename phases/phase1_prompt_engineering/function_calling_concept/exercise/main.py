"""EXERCISE -- Function Calling Schema.

Practice: a tool schema tells the model a function's name and arguments.

Task: fill in GRADE_TOOL_SCHEMA for calculate_grade(scores, weights).

Check your work with:
    python phases/phase1_prompt_engineering/function_calling_concept/solution/check.py
"""

GRADE_TOOL_SCHEMA: dict = {}
# TODO: give it "type": "function" and a "function" dict with "name": "calculate_grade",
# a "description", and "parameters" whose "properties" are the arrays "scores" and
# "weights" (type "number" items), both listed in "required".


if __name__ == "__main__":
    print(GRADE_TOOL_SCHEMA)
