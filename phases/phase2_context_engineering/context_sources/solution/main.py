"""SOLUTION -- Context Sources.

Reference answer: prepend date, name and goal to the tutor persona.
"""

from datetime import datetime


def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    """Return metadata lines (date, name, goal) followed by the tutor persona."""
    if date_str is None:
        date_str = datetime.now().strftime("%A, %B %d, %Y")
    return "\n".join([
        f"Today is {date_str}.",
        f"The student's name is {name}.",
        f"Current study goal: {goal}.",
        "",
        "You are Study Buddy, a patient tutor.",
    ])


if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam", "Monday, Oct 1"))
