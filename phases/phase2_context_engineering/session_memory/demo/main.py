"""DEMO -- Session Memory in app/memory.py.

Live-code target: manage multi-turn history using app.memory, verifying that
turns accumulate and can be retrieved or cleared.

Run:
    python phases/phase2_context_engineering/session_memory/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app import memory

SESSION_ID = "demo-session-123"

print("=" * 60)
print(f"SESSION MEMORY DEMO (session_id={SESSION_ID})")
print("=" * 60)

# Clear any previous run
memory.clear(SESSION_ID)
print("Initial history length:", len(memory.get_history(SESSION_ID)))

# Simulate turn 1
print("\nTurn 1: Student mentions they're studying cellular respiration")
memory.append(SESSION_ID, "user", "I am studying cellular respiration.")
memory.append(SESSION_ID, "assistant", "Great! What stage would you like to review?")

# Simulate turn 2
print("Turn 2: Student asks about ATP production")
memory.append(SESSION_ID, "user", "How much ATP does the electron transport chain produce?")
memory.append(SESSION_ID, "assistant", "It produces roughly 30 to 32 ATP molecules.")

history = memory.get_history(SESSION_ID)
print(f"\nRetrieved {len(history)} messages from session store:")
for i, msg in enumerate(history, 1):
    print(f"  [{i}] {msg['role']:9s}: {msg['content']}")

# Clear session
memory.clear(SESSION_ID)
print("\nAfter memory.clear():", len(memory.get_history(SESSION_ID)), "messages remaining.")
