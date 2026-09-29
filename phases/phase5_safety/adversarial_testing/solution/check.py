"""Self-check for the Red-Teaming the Input Guard exercise.

    python .../adversarial_testing/solution/check.py [--solution]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("redteam_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["redteam_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    results = module.run_redteam_tests()
    assert results.get("attacks_blocked") is True, "the filter must block every attack"
    assert results.get("benign_allowed") is True, "the filter must not block benign text"

    print("OK - blocked both attacks and allowed the benign question")


if __name__ == "__main__":
    main()
