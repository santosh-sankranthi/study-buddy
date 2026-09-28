"""Self-check for Phase 1.5 Function Calling Concept."""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    schema = getattr(mod, "GRADE_TOOL_SCHEMA", {})
    assert schema.get("type") == "function", "TODO(1): Schema type must be 'function'"
    fn = schema.get("function", {})
    assert fn.get("name") == "calculate_grade", "Tool name must be 'calculate_grade'"
    params = fn.get("parameters", {}).get("properties", {})
    assert "scores" in params and "weights" in params, "Parameters must include 'scores' and 'weights'"

    print(f"✅ Function calling concept check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
