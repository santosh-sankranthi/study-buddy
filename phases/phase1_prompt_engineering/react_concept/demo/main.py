"""DEMO -- ReAct Loop Simulation.

Live-code target: trace a 2-step ReAct agent by simulating the interaction between
thoughts, actions, and environment observations.

Run:
    python phases/phase1_prompt_engineering/react_concept/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import get_exam_schedule, search_notes

GOAL = "Find when the Biology exam is and what topics to focus on."

print("=" * 60)
print(f"Agent Goal: {GOAL}")
print("=" * 60)

trace = []

# Step 1: Look up exam date
thought_1 = "I need to check the date for the Biology exam."
action_1 = "get_exam_schedule(subject='biology')"
obs_1 = get_exam_schedule("biology")
trace.append({"thought": thought_1, "action": action_1, "observation": obs_1})

print(f"\n[Step 1]")
print(f"  Thought:     {thought_1}")
print(f"  Action:      {action_1}")
print(f"  Observation: {obs_1}")

# Step 2: Look up study topics
thought_2 = "Now that I have the exam date, I need to check study notes for key topics."
action_2 = "search_notes(query='biology key topics')"
obs_2 = "Key topics: Cellular respiration, photosynthesis, and genetics."
trace.append({"thought": thought_2, "action": action_2, "observation": obs_2})

print(f"\n[Step 2]")
print(f"  Thought:     {thought_2}")
print(f"  Action:      {action_2}")
print(f"  Observation: {obs_2}")

# Step 3: Finish
thought_3 = "I have both the exam date and recommended topics. I can formulate the final answer."
final_answer = f"{obs_1} To prepare, focus on: {obs_2}"
action_3 = f"FINISH(answer='{final_answer}')"
trace.append({"thought": thought_3, "action": action_3, "observation": None})

print(f"\n[Step 3 (Finish)]")
print(f"  Thought:     {thought_3}")
print(f"  Action:      {action_3}")
print("\n" + "=" * 60)
print(f"Final Output: {final_answer}")
print("=" * 60)
