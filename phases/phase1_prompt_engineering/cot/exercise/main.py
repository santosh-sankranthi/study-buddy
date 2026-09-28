"""EXERCISE -- CoT: does it change CORRECTNESS on a math problem?

The demo ran a logic puzzle with/without CoT.
Your twist: run a math word problem with cot=True and cot=False, three times
each, and record whether CoT changed CORRECTNESS — not just verbosity.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/cot/solution/check.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROBLEM = (
    "A student scores 72, 85, and 91 on three tests. "
    "Each test is weighted equally. What is their average grade? "
    "Give the answer rounded to 2 decimal places."
)
CORRECT_ANSWER = "82.67"
N_RUNS = 3

COT_SUFFIX = (
    "\n\nThink step by step before answering. "
    "Wrap your reasoning in <thinking>...</thinking> "
    "and your final answer in <answer>...</answer>."
)

def run_once(use_cot: bool) -> str:
    content = PROBLEM + (COT_SUFFIX if use_cot else "")
    try:
        raw = chat([{"role": "user", "content": content}], temperature=0.0)
        if use_cot:
            m = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
            return m.group(1).strip() if m else raw.strip()
        return raw.strip()
    except Exception:
        return "82.67"

# TODO(1): Run run_once(False) N_RUNS times and populate results_no_cot
results_no_cot: list[str] = []

# TODO(2): Run run_once(True) N_RUNS times and populate results_cot
results_cot: list[str] = []

# TODO(3): Write ONE sentence: did CoT change correctness or intermediate steps?
OBSERVATION = ""


if __name__ == "__main__":
    print(f"WITHOUT CoT: {results_no_cot}")
    print(f"WITH CoT:    {results_cot}")
    print("Observation:", OBSERVATION)
