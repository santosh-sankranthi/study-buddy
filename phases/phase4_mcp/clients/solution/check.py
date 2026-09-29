"""Self-check for the MCP Clients exercise.

    python .../clients/solution/check.py             # checks your exercise
    python .../clients/solution/check.py --solution  # checks the reference
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("clients_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["clients_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    res = module.call_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]})
    assert "91.5" in res, f"expected weighted grade 91.5, got {res!r}"
    assert "75" in module.call_tool("calculate_grade", {"scores": [100.0, 50.0], "weights": [0.5, 0.5]})

    print(f"OK - call_tool dispatched calculate_grade -> {res!r}")


if __name__ == "__main__":
    main()
