"""EXERCISE -- Tool Schema Shape: calculate_grade.

The demo registered search_notes and get_exam_schedule schemas.
Your twist: write the tool schema dict for calculate_grade.

Run when done:
    python phases/phase1_prompt_engineering/function_calling_concept/solution/check.py
"""
# TODO(1): Define GRADE_TOOL_SCHEMA dict adhering to the OpenAI function calling schema format:
# {
#     "type": "function",
#     "function": {
#         "name": "calculate_grade",
#         "description": "...",
#         "parameters": { ... scores and weights array properties ... },
#         "required": ["scores", "weights"],
#     }
# }

GRADE_TOOL_SCHEMA: dict = {}

if __name__ == "__main__":
    print(GRADE_TOOL_SCHEMA)
