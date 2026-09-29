"""EXERCISE -- Chain of Thought.

Practice: ask the model to reason step by step, then read its final answer.

Task: fill in cot_prompt() and extract_answer().

Check your work with:
    python phases/phase1_prompt_engineering/cot/solution/check.py
"""

PROBLEM = "A student scores 72, 85, and 91. What is the average, to 2 decimal places?"
COT_SUFFIX = "\n\nThink step by step. Put your final answer in <answer>...</answer>."


def cot_prompt(problem: str) -> str:
    """Return `problem` with the step-by-step instruction appended."""
    # TODO(1): append COT_SUFFIX to the problem.
    raise NotImplementedError("cot_prompt")


def extract_answer(reply: str) -> str:
    """Return the text inside <answer>...</answer>, or `reply` if there are no tags."""
    # TODO(2): find the <answer> tag and return its contents.
    raise NotImplementedError("extract_answer")


if __name__ == "__main__":
    print(cot_prompt(PROBLEM))
