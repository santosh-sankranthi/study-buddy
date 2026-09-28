import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES = REPO_ROOT / "phases"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── 1. Phase 2: mcp_concept ───────────────────────────────────────────────────
write(
    PHASES / "phase2_context_engineering/mcp_concept/explainer.md",
    """# 2.6 — Model Context Protocol (MCP) Concept

## What was broken before
Right now, every time we want Study Buddy to connect to external data or tools, we write bespoke, hand-crafted Python glue code. If another application (like Claude Desktop or Cursor) wants to access our course notes or tools, we would have to rewrite the integration entirely.

## How it works
Model Context Protocol (MCP) is an open, standardized protocol (like USB-C for AI applications) that lets any host app communicate with any tool or data provider over JSON-RPC. A server exposes tools and resources; any compliant client can discover and use them without knowing how they were implemented.

We will build a real MCP server and client in **Phase 7**. For now, remember: tools and resources can be decoupled from the application and served over a universal protocol.
"""
)

# ── 2. Phase 5: embedding explainer ───────────────────────────────────────────
write(
    PHASES / "phase5_rag_pipeline/embedding/explainer.md",
    """# 5.2 — Embedding in RAG (Plumbing Reuse)

## What was broken before
In Phase 3 and 4, we built vector embeddings and stored them in ChromaDB. In RAG, we don't reinvent embedding: we reuse that exact vector pipeline to turn student queries into query vectors that match indexed chunk vectors.

## How it works
When the user asks a question, we call `embed(question)` (or batch embed). The resulting vector is compared against chunk embeddings in ChromaDB using cosine distance. Consistent embedding dimensions and model selection are critical — never mix different embedding models within the same vector store.
"""
)

# ── 3. Phase 6: tools (6.1) ───────────────────────────────────────────────────
tools_dir = PHASES / "phase6_agents_and_tools/tools"
write(
    tools_dir / "explainer.md",
    """# 6.1 — Tools (Execution-Wired)

## What was broken before
In Phase 1.5, we wrote tool schemas (`TOOLS`), but they were just JSON blueprints. If an LLM decided to call `search_notes` or `calculate_grade`, our app had no code to actually run them!

## How it works
We build a `TOOL_REGISTRY` — a Python dictionary mapping function names (`str`) to callable Python functions. When the model requests a tool call, we look up the name in the registry and execute it with the provided arguments.
"""
)

write(
    tools_dir / "demo/main.py",
    """\"\"\"DEMO -- Wiring Tool Registry for Execution.

The instructor demonstrates registering real Python functions into TOOL_REGISTRY.
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOL_REGISTRY, get_exam_schedule, search_notes

print("Registered tools in TOOL_REGISTRY:")
for name, fn in TOOL_REGISTRY.items():
    print(f"  • {name}: {fn.__doc__.strip().splitlines()[0] if fn.__doc__ else 'callable'}")

# Test invoking directly through the registry
print("\nTesting get_exam_schedule directly:")
print("  Result:", TOOL_REGISTRY["get_exam_schedule"](subject="biology"))
"""
)

write(
    tools_dir / "exercise/main.py",
    """\"\"\"EXERCISE -- Wire calculate_grade into TOOL_REGISTRY.

The demo registered search_notes and get_exam_schedule.
Your twist: implement calculate_grade and wire it into TOOL_REGISTRY.

Run when done:
    python phases/phase6_agents_and_tools/tools/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): In app/tools.py (or implement below for self-check):
#   Implement calculate_grade(scores: list[float], weights: list[float]) -> str
#   - Check that len(scores) == len(weights)
#   - Calculate weighted average: sum(s * w) / sum(w)
#   - Return string: "Weighted average: <grade>%"

def calculate_grade(scores: list[float], weights: list[float]) -> str:
    raise NotImplementedError("TODO(1): implement calculate_grade")


# TODO(2): Register calculate_grade in TOOL_REGISTRY
# TOOL_REGISTRY["calculate_grade"] = calculate_grade


if __name__ == "__main__":
    scores = [80.0, 90.0, 70.0]
    weights = [0.3, 0.4, 0.3]
    result = calculate_grade(scores, weights)
    print("Calculated grade:", result)
"""
)

write(
    tools_dir / "solution/main.py",
    """\"\"\"SOLUTION -- Wire calculate_grade into TOOL_REGISTRY.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import TOOL_REGISTRY, calculate_grade

if __name__ == "__main__":
    scores = [80.0, 90.0, 70.0]
    weights = [0.3, 0.4, 0.3]
    res = calculate_grade(scores, weights)
    print("Solution calculated grade:", res)
    assert "calculate_grade" in TOOL_REGISTRY
"""
)

write(
    tools_dir / "solution/check.py",
    """\"\"\"Self-check for Phase 6.1 Tools exercise.\"\"\"
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("tools_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "calculate_grade", None)
    assert fn is not None, "calculate_grade function must be defined"

    # Test execution
    res = fn([80.0, 90.0, 70.0], [0.3, 0.4, 0.3])
    assert isinstance(res, str), "Result must be a string"
    assert "80" in res or "81" in res or "%" in res, f"Expected grade in result, got: {res}"

    print(f"✅ Tools check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── 4. Phase 6: agent_loops (6.4) ─────────────────────────────────────────────
loops_dir = PHASES / "phase6_agents_and_tools/agent_loops"
write(
    loops_dir / "explainer.md",
    """# 6.4 — Agent Loops & Termination Guards

## What was broken before
A single ReAct step is not an autonomous agent — the model must be allowed to iterate in a loop until it reaches a conclusion (`FINISH`). However, autonomous loops risk infinite loops, rapid token depletion, and huge API bills if the model repeats the same action over and over.

## How it works
An agent loop wraps tool execution in a bounded loop (`while not done:` or `for step in range(MAX_STEPS):`). We implement two critical safety guards:
1. A hard iteration cap (`MAX_STEPS = 10`)
2. Same-tool-twice loop detection (halting if the exact same tool and arguments are executed back-to-back).
"""
)

write(
    loops_dir / "demo/main.py",
    """\"\"\"DEMO -- Agent Loop with Hard Iteration Cap.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import agent_loop

print("Running agent loop on an exam query:")
res = agent_loop("When is the biology exam?")
print("Result answer:", res.get("answer"))
print("Total steps:", res.get("steps"))
print("Halted early:", res.get("halted"))
"""
)

write(
    loops_dir / "exercise/main.py",
    """\"\"\"EXERCISE -- Same-Tool Loop Detection.

The demo capped iterations at MAX_STEPS. Your twist: implement loop detection
so that if the same tool is called with identical arguments twice in a row,
the loop halts immediately with reason='loop_detected'.

Run when done:
    python phases/phase6_agents_and_tools/agent_loops/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement loop_detector(history: list[dict]) -> bool
#   Given a list of tool calls [{'name': str, 'arguments': str}],
#   return True if the last tool call is identical to the preceding one.

def detect_repetition(tool_calls: list[dict]) -> bool:
    raise NotImplementedError("TODO(1): implement detect_repetition")


# TODO(2): Write one sentence explaining why loop detection is critical in production:
OBSERVATION = ""


if __name__ == "__main__":
    sample_calls = [
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    ]
    print("Repetition detected:", detect_repetition(sample_calls))
"""
)

write(
    loops_dir / "solution/main.py",
    """\"\"\"SOLUTION -- Same-Tool Loop Detection.\"\"\"
def detect_repetition(tool_calls: list[dict]) -> bool:
    if len(tool_calls) < 2:
        return False
    prev = tool_calls[-2]
    curr = tool_calls[-1]
    return (prev.get("name") == curr.get("name")) and (prev.get("arguments") == curr.get("arguments"))

OBSERVATION = "Loop detection prevents infinite recursive API calls and quota depletion when models hallucinate stagnant reasoning loops."

if __name__ == "__main__":
    calls = [
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    ]
    print("Detected:", detect_repetition(calls))
"""
)

write(
    loops_dir / "solution/check.py",
    """\"\"\"Self-check for Agent Loops exercise.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("loops_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "detect_repetition", None)
    assert fn is not None, "detect_repetition must be defined"

    calls_same = [
        {"name": "search", "arguments": "q1"},
        {"name": "search", "arguments": "q1"}
    ]
    calls_diff = [
        {"name": "search", "arguments": "q1"},
        {"name": "search", "arguments": "q2"}
    ]

    assert fn(calls_same) is True, "Must return True for identical consecutive calls"
    assert fn(calls_diff) is False, "Must return False for different consecutive calls"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write OBSERVATION"

    print(f"✅ Agent loops check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

print("Created Phase 6 tools and agent_loops successfully.")
