"""Self-check for the MCP Servers exercise.

    python .../servers/solution/check.py             # checks your exercise
    python .../servers/solution/check.py --solution  # checks the reference
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("servers_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["servers_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    server = {}
    assert module.register_grade_tool(server) is True, "must return True"
    assert "calculate_grade" in server, "calculate_grade must be registered"
    assert "75" in server["calculate_grade"]([100.0, 50.0], [0.5, 0.5])

    print(f"OK - server exposes {sorted(server)}")


if __name__ == "__main__":
    main()
