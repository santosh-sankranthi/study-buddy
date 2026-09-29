"""Self-check for the ReAct Loop exercise.

    python .../react_loop/solution/check.py             # checks your exercise
    python .../react_loop/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mod_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    messages = [{"role": "user", "content": "When is the biology exam?"}]
    tool_call = {"id": "call_1", "type": "function",
                 "function": {"name": "get_exam_schedule", "arguments": '{"subject": "biology"}'}}

    updated = module.apply_tool_call(messages, tool_call)
    assert len(updated) == 3, "expected one new assistant message and one new tool message"
    assert updated[-2]["role"] == "assistant" and updated[-2]["tool_calls"] == [tool_call]
    assert updated[-1]["role"] == "tool" and updated[-1]["tool_call_id"] == "call_1"
    assert "2026-11-15" in updated[-1]["content"], "the tool should return the real exam date"
    assert len(messages) == 1, "apply_tool_call must not mutate the input list"

    print(f"OK - appended observation: {updated[-1]['content']}")


if __name__ == "__main__":
    main()
