"""Self-check for the Output Moderation exercise.

    python .../moderation/solution/check.py [--solution]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("moderation_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["moderation_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    safe = module.moderate_assistant_output("Cellular respiration generates ATP.")
    assert safe["flagged"] is False and safe["status"] == "APPROVED", safe

    unsafe = module.moderate_assistant_output("Here is an attack plan to kill people with a bomb.")
    assert unsafe["flagged"] is True and unsafe["status"] == "BLOCKED", unsafe

    print("OK - approved a safe answer and blocked a harmful one")


if __name__ == "__main__":
    main()
