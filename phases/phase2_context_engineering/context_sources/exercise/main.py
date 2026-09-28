"""EXERCISE -- Context Sources: Metadata Injection.

The demo inspected token distribution per role.
Your twist: implement build_personalized_system_prompt() to inject
the student's name, study goal, and current date at the top of the prompt.

Run when done:
    python phases/phase2_context_engineering/context_sources/solution/check.py
"""
from datetime import datetime

# TODO(1): Implement build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str
# Format:
#   Today is <date_str>.
#   The student's name is <name>.
#   Current study goal: <goal>.
#   <Base tutor persona>

def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    raise NotImplementedError("TODO(1): implement build_personalized_system_prompt")

if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam"))
