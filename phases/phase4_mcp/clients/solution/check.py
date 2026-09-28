"""Self-check for Phase 4.3 MCP Clients."""
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
    spec = importlib.util.spec_from_file_location("cli_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    res = getattr(mod, "grade_result", "")
    assert isinstance(res, str) and len(res.strip()) > 0, "grade_result must be a non-empty string"
    assert "91" in res or "92" in res or "%" in res, f"Expected grade percentage, got: {res}"

    print(f"✅ MCP Clients check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
