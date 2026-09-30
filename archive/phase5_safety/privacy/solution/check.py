"""Self-check for the PII Scrubbing exercise.

    python .../privacy/solution/check.py [--solution]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("privacy_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["privacy_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    clean, types = module.scrub_international_phone("Call +91 9876543210 or +44 7911123456")
    assert "PHONE_IN" in types and "PHONE_UK" in types, "detect both phone types"
    assert "+91" not in clean and "+44" not in clean, "redact the numbers"

    print("OK - redacted PHONE_IN and PHONE_UK")


if __name__ == "__main__":
    main()
