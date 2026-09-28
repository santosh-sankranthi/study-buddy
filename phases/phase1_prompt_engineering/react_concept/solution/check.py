"""Self-check for Phase 1.6 ReAct Concept."""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    doc = (TARGET / "solution" / "trace.md") if args.solution else (TARGET / "exercise" / "trace.md")
    content = doc.read_text(encoding="utf-8")

    t_cnt = content.count("Thought:")
    a_cnt = content.count("Action:")
    o_cnt = content.count("Observation:")

    assert t_cnt >= 3, f"Expected at least 3 Thought: steps, found {t_cnt}"
    assert a_cnt >= 3, f"Expected at least 3 Action: steps, found {a_cnt}"
    assert "FINISH(" in content, "Trace must end with Action: FINISH(answer=...)"

    if not args.solution:
        assert "TODO" not in content, "Please complete the trace steps in trace.md"

    print(f"✅ ReAct concept check passed ({doc.name})!")

if __name__ == "__main__":
    main()
