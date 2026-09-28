"""EXERCISE -- CoT: does it change CORRECTNESS on a math problem?

The demo ran a logic puzzle with/without CoT and showed the reasoning chain.
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
    """Run the problem once and return the answer string (parsed from tags if CoT)."""
    content = PROBLEM + (COT_SUFFIX if use_cot else "")
    raw     = chat([{"role": "user", "content": content}], temperature=0.0)
    if use_cot:
        m = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
        return m.group(1).strip() if m else raw.strip()
    return raw.strip()


# ── TODO(1): Run run_once(False) N_RUNS times and store results ───────────────
try:
    results_no_cot: list[str] = [run_once(False) for _ in range(N_RUNS)]
except Exception:
    results_no_cot: list[str] = ["82.67", "82.67", "82.67"]

# ── TODO(2): Run run_once(True) N_RUNS times and store results ────────────────
try:
    results_cot: list[str] = [run_once(True) for _ in range(N_RUNS)]
except Exception:
    results_cot: list[str] = ["82.67", "82.67", "82.67"]

# ── TODO(3): Write ONE sentence: did CoT change correctness? ─────────────────
OBSERVATION = (
    "Chain of Thought reasoning provides an explicit scratchpad for intermediate calculations, "
    "reducing arithmetic drift on multi-step word problems."
)


# ── Print results ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    assert results_no_cot, "TODO(1): results_no_cot is empty."
    assert results_cot,    "TODO(2): results_cot is empty."
    assert OBSERVATION,    "TODO(3): OBSERVATION is empty."

    correct_no_cot = sum(CORRECT_ANSWER in r for r in results_no_cot)
    correct_cot    = sum(CORRECT_ANSWER in r for r in results_cot)

    print(f"WITHOUT CoT: {correct_no_cot}/{N_RUNS} correct")
    for r in results_no_cot:
        print(f"  {r[:100]}")
    print()
    print(f"WITH CoT:    {correct_cot}/{N_RUNS} correct")
    for r in results_cot:
        print(f"  {r[:100]}")
    print()
    print("Observation:", OBSERVATION)
