"""DEMO -- Agent Loop with Hard Iteration Cap."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import agent_loop

print("Running agent loop on an exam query:")
res = agent_loop("When is the biology exam?")
print("Result answer:", res.get("answer"))
print("Total steps:", res.get("steps"))
print("Halted early:", res.get("halted"))
