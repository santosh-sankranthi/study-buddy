"""DEMO -- Chain of Thought (CoT).

Live-code target: run the SAME logic puzzle with and without "think step by
step", show the correctness difference, then wire the cot flag and <thinking>
tag parsing into app/main.py.

Run:
    python phases/phase1_prompt_engineering/cot/demo/main.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PUZZLE = (
    "Three students — Alice, Bob, and Carol — sit in a row. "
    "Alice is not next to Bob. Bob is not next to Carol. "
    "Who is in the middle?"
)

# ── Without CoT ───────────────────────────────────────────────────────────────
print("=" * 60)
print("WITHOUT CoT:")
print("=" * 60)
print("Puzzle:", PUZZLE)
answer_raw = chat([{"role": "user", "content": PUZZLE}], temperature=0.0)
print("Answer:", answer_raw)

# ── With CoT tags ─────────────────────────────────────────────────────────────
COT_SUFFIX = (
    "\n\nThink step by step before answering. "
    "Wrap your reasoning in <thinking>...</thinking> "
    "and your final answer in <answer>...</answer>."
)

print("\n" + "=" * 60)
print("WITH CoT (<thinking> + <answer> tags):")
print("=" * 60)
raw_cot = chat([{"role": "user", "content": PUZZLE + COT_SUFFIX}], temperature=0.0)

thinking = re.search(r"<thinking>(.*?)</thinking>", raw_cot, re.DOTALL)
answer   = re.search(r"<answer>(.*?)</answer>",   raw_cot, re.DOTALL)

if thinking:
    print("Reasoning:")
    print(thinking.group(1).strip())
    print()
print("Final answer:", answer.group(1).strip() if answer else raw_cot)

print("\n── What changed ─────────────────────────────────────────────")
print("  No CoT: model may jump to a wrong conclusion.")
print("  CoT:    model writes the reasoning first; answer is better supported.")
print()
print("Next: open app/main.py and add the cot: bool field to AskRequest.")
print("      When True, append COT_SUFFIX and parse <thinking>/<answer> tags.")
