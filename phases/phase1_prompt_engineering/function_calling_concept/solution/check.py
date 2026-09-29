"""Self-check for the Function Calling Schema exercise: python check.py [--solution]."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT = HERE.parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location("function_calling_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["function_calling_under_test"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target = CONCEPT / ("solution" if args.solution else "exercise") / "main.py"
    module = load(target)

    schema = module.GRADE_TOOL_SCHEMA
    assert schema["type"] == "function", "type must be 'function'"
    function = schema["function"]
    assert function["name"] == "calculate_grade"
    parameters = function["parameters"]
    assert parameters["properties"]["scores"]["type"] == "array"
    assert parameters["properties"]["weights"]["items"]["type"] == "number"
    assert set(parameters["required"]) == {"scores", "weights"}
    print("OK - GRADE_TOOL_SCHEMA describes calculate_grade with two required arrays")


if __name__ == "__main__":
    main()
