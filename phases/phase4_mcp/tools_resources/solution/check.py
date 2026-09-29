"""Self-check for the MCP Tools & Resources exercise.

    python .../tools_resources/solution/check.py             # checks your exercise
    python .../tools_resources/solution/check.py --solution  # checks the reference
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("resources_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["resources_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    data = json.loads(module.get_quiz_attempts("session_123"))
    assert data["session_id"] == "session_123"
    assert len(data["attempts"]) == 2
    assert data["attempts"][0]["correct"] is True

    print(f"OK - resource returned {len(data['attempts'])} attempts for session_123")


if __name__ == "__main__":
    main()
