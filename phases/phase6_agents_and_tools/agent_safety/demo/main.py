"""DEMO -- Agent Loop Detection & Safety Halting.

Live-code target: simulate agent action streams and demonstrate how
loop detection halts thrashing before max steps are exhausted.

Run:
    python phases/phase6_agents_and_tools/agent_safety/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

print("=" * 60)
print("AGENT LOOP DETECTION & SAFETY DEMO")
print("=" * 60)

# Simulate an agent stuck in a repetitive loop
action_stream = [
    "search_notes({'query': 'photosynthesis'})",
    "search_notes({'query': 'photosynthesis'})",  # Duplicate! Loop detected.
    "search_notes({'query': 'photosynthesis'})",
]

last_action = None
halted = False
reason = "done"

for step, action in enumerate(action_stream, 1):
    print(f"\nStep {step}: Emitting action -> {action}")
    if action == last_action and last_action not in (None, "", "FINISH"):
        halted = True
        reason = "loop_detected"
        print("  🚨 LOOP DETECTED: Agent repeated exact same action back-to-back!")
        print("  Halting agent immediately to conserve tokens.")
        break
    last_action = action

print("\n" + "=" * 60)
print(f"Agent Execution Summary: Halted={halted}, Reason={reason}")
print("=" * 60)
