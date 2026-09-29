"""SOLUTION -- Chain of Thought."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat  # noqa: E402

PROBLEM = "A student scores 72, 85, and 91. What is the average, to 2 decimal places?"
COT_SUFFIX = "\n\nThink step by step. Put your final answer in <answer>...</answer>."


def cot_prompt(problem: str) -> str:
    return problem + COT_SUFFIX


def extract_answer(reply: str) -> str:
    match = re.search(r"<answer>(.*?)</answer>", reply, re.DOTALL)
    return match.group(1).strip() if match else reply.strip()


def answer(problem: str) -> str:
    reply = chat([{"role": "user", "content": cot_prompt(problem)}], temperature=0.0)
    return extract_answer(reply)


if __name__ == "__main__":
    print(answer(PROBLEM))
