"""Self-check for the Prompt Injection Scan exercise.

    python .../prompt_injection/solution/check.py [--solution]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("injection_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["injection_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    results = module.scan_batch_for_injections()
    assert len(results) == len(module.TEST_MATRIX), "scan every item in the matrix"
    for item in results:
        assert item["flagged"] == item["expected"], f"wrong verdict for {item['text']!r}"

    print(f"OK - flagged {sum(r['flagged'] for r in results)} injections, benign text passed")


if __name__ == "__main__":
    main()
