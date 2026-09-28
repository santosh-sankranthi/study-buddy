"""SOLUTION -- Context Sources: Metadata Injection."""
from datetime import datetime

def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    if date_str is None:
        date_str = datetime.now().strftime("%A, %B %d, %Y")
    lines = [
        f"Today is {date_str}.",
        f"The student's name is {name}.",
        f"Current study goal: {goal}.",
        "",
        "You are Study Buddy, a patient tutor.",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam"))
