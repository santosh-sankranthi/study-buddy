"""DEMO -- Multi-Agent Pipeline: Planner, Executor, Critic.

Live-code target: run app.agent.plan_and_execute() across a multi-part study goal,
observe step decomposition, sub-task execution, and critic evaluations.

Run:
    python phases/phase3_agents_and_tools/multi_agent/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import critic, planner

GOAL = "Prepare a study schedule for Biology and calculate current grade for scores [80, 90] with weights [0.5, 0.5]."

print("=" * 60)
print("MULTI-AGENT PIPELINE DEMO")
print(f"Goal: {GOAL}")
print("=" * 60)

# 1. Planner Agent
plan = planner(GOAL)
print(f"\n1. Planner Agent decomposed goal into {len(plan)} step(s):")
for i, step in enumerate(plan, 1):
    print(f"   [{i}] {step}")

# 2. Critic Agent evaluation demo
sample_step = "Check date for Biology exam."
good_result = "Biology exam is scheduled for 2026-11-15."
bad_result = "Photosynthesis takes place in chloroplasts."

print("\n2. Critic Agent Evaluation:")
app_good, reason_good = critic(sample_step, good_result)
print(f"   Candidate 1: '{good_result}'")
print(f"   -> Approved: {app_good} ({reason_good})")

app_bad, reason_bad = critic(sample_step, bad_result)
print(f"\n   Candidate 2: '{bad_result}'")
print(f"   -> Approved: {app_bad} ({reason_bad})")
