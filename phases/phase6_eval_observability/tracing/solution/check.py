"""Self-check for the Trace Summary exercise.

    .../tracing/solution/check.py             # checks your exercise
    .../tracing/solution/check.py --solution  # checks the reference
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("trace_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["trace_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()
    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    summary = module.summarize_trace(module.SAMPLE_SPANS)
    assert summary["total_duration_ms"] == 1615
    assert summary["total_tokens"] == 635
    assert abs(summary["total_cost_usd"] - 0.000317) < 1e-9
    print("OK - trace totals summed correctly")


if __name__ == "__main__":
    main()
