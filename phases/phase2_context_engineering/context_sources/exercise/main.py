"""EXERCISE -- Context Sources.

Practice: inject today's date, the student's name and goal into a system prompt.

Task: finish build_personalized_system_prompt() to prepend those metadata lines.

Check your work with:
    python phases/phase2_context_engineering/context_sources/solution/check.py
"""


def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    """Return metadata lines (date, name, goal) followed by the tutor persona."""
    # TODO: default date_str to today (from datetime import datetime) when it is
    # None, then join and return these lines:
    #   Today is <date>.
    #   The student's name is <name>.
    #   Current study goal: <goal>.
    #   <blank>
    #   You are Study Buddy, a patient tutor.
    raise NotImplementedError("build_personalized_system_prompt")


if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam", "Monday, Oct 1"))
