"""EXERCISE -- Running and Analyzing the ReAct Loop.

The demo ran agent_loop() for a single schedule query.
Your twist: execute agent_loop() for Biology exam schedule inquiry,
verify that trace steps contain valid Thought/Action/Observation records,
and verify that the agent reached a clean finish (halted=False).

Fill in every TODO. Run when done:
    python phases/phase6_agents_and_tools/react_loop/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import agent_loop


# ── TODO(1): Execute agent loop for Biology query ────────────────────────────
def run_biology_query(query: str = "When is the Biology exam?") -> dict:
    """Call agent_loop(query) and return the full result dictionary."""
    # TODO(1): return agent_loop(query)
    return agent_loop(query)


# ── TODO(2): Inspect trace structure ─────────────────────────────────────────
def validate_trace_structure(result: dict) -> bool:
    """Return True if every step in trace has 'thought', 'action', and 'observation'."""
    trace = result.get("trace", [])
    if not trace:
        return False
    # TODO(2): check all s in trace have 'thought', 'action', 'observation' keys
    return all("thought" in s and "action" in s and "observation" in s for s in trace)


if __name__ == "__main__":
    res = run_biology_query()
    print("Answer:", res["answer"])
    print("Valid trace structure:", validate_trace_structure(res))
    print(f"Executed in {res['steps']} steps.")
