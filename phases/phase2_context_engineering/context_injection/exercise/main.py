"""EXERCISE -- Dynamic Context & Metadata Injection.

The demo injected current date and student name into the system prompt.
Your twist: implement a dynamic metadata builder that injects:
1. Current date
2. Student name
3. Student study goal
and returns a full messages list suitable for chat(), then verify with context_report.

Fill in every TODO. Run when done:
    python phases/phase2_context_engineering/context_injection/solution/check.py
"""

from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.context import context_report
from app.prompts import TUTOR_SYSTEM_PROMPT


# ── TODO(1): Implement build_personalized_system_prompt ──────────────────────
def build_personalized_system_prompt(
    student_name: str | None,
    study_goal: str | None,
    current_date: str | None = None,
) -> str:
    """Construct system prompt with prepended date, student name, and study goal lines."""
    parts = []
    # TODO(1a): if current_date is provided, add "Today is {current_date}."
    if current_date:
        parts.append(f"Today is {current_date}.")
    # TODO(1b): if student_name is provided, add "The student's name is {student_name}."
    if student_name:
        parts.append(f"The student's name is {student_name}.")
    # TODO(1c): if study_goal is provided, add "Student goal: {study_goal}."
    if study_goal:
        parts.append(f"Student goal: {study_goal}.")

    parts.append(TUTOR_SYSTEM_PROMPT)
    return "\n".join(parts)


# ── TODO(2): Build complete messages list and analyze context breakdown ──────
def create_session_payload(
    question: str,
    student_name: str = "Bob",
    study_goal: str = "Pass AP Biology exam",
) -> dict:
    """Return dict with 'messages' list and 'context_report'."""
    today = datetime.now().strftime("%A, %B %d, %Y")
    sys_content = build_personalized_system_prompt(student_name, study_goal, today)
    messages = [
        {"role": "system", "content": sys_content},
        {"role": "user", "content": question},
    ]
    report = context_report(messages)
    return {"messages": messages, "context_report": report}


if __name__ == "__main__":
    payload = create_session_payload("What is cellular respiration?")
    print("Generated Context Report:")
    for role, cnt in payload["context_report"].items():
        print(f"  {role:10s}: {cnt} tokens")
    print("\nSystem Prompt Sample:")
    print(payload["messages"][0]["content"][:200], "...")
