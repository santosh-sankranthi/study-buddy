"""DEMO -- Context Compaction in app/memory.py.

Live-code target: observe how compact_if_needed compresses older messages into a summary
when token count exceeds budget, preserving conversational continuity at lower token cost.

Run:
    python phases/phase2_context_engineering/context_compaction/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app import memory

SESSION = "demo-compaction"
memory.clear(SESSION)

print("=" * 60)
print(f"CONTEXT COMPACTION DEMO (session_id={SESSION})")
print("=" * 60)

# Simulate 6 messages about organic chemistry
memory.append(SESSION, "user", "I need to prepare for my Organic Chemistry exam.")
memory.append(SESSION, "assistant", "Sure! We can cover functional groups, resonance, and reaction mechanisms.")
memory.append(SESSION, "user", "Let's focus on SN1 and SN2 reaction mechanisms.")
memory.append(SESSION, "assistant", "SN1 is a two-step mechanism via a carbocation; SN2 is a one-step concerted mechanism with backside attack.")
memory.append(SESSION, "user", "What solvent favors SN2?")
memory.append(SESSION, "assistant", "Polar aprotic solvents like acetone or DMSO favor SN2.")

before = memory.get_history(SESSION)
print(f"\nBefore compaction: {len(before)} messages")
for m in before:
    print(f"  {m['role']:9s}: {m['content'][:60]}...")

# Compact with small budget threshold to force summarization
print("\nRunning compact_if_needed(budget=50)...")
compacted = memory.compact_if_needed(SESSION, budget=50)
after = memory.get_history(SESSION)

print(f"\nCompacted? {compacted}")
print(f"After compaction: {len(after)} messages (reduced from {len(before)})")
for m in after:
    print(f"  {m['role']:9s}: {m['content'][:75]}...")
