"""DEMO -- Autonomous ReAct Agent Loop.

Live-code target: execute app.agent.agent_loop() on a real user question,
inspect the accumulated Thought/Action/Observation trace, and examine how
the agent self-terminates when it has gathered sufficient context.

Run:
    python phases/phase3_agents_and_tools/react_loop/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import agent_loop

QUESTION = "When is the Math exam scheduled?"

print("=" * 60)
print(f"AGENT LOOP DEMO: '{QUESTION}'")
print("=" * 60)

result = agent_loop(QUESTION)

print(f"\nFinal Answer: {result['answer']}")
print(f"Total Steps:  {result['steps']}")
print(f"Halted?       {result['halted']} (Reason: {result['reason']})")

print("\n--- Execution Trace ---")
for i, step in enumerate(result["trace"], 1):
    print(f"\nStep {i}:")
    print(f"  Thought:     {step['thought']}")
    print(f"  Action:      {step['action']}")
    print(f"  Observation: {step['observation']}")
