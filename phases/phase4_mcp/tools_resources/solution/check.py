"""Self-check for Phase 4.2 MCP Tools & Resources."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("res_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "get_quiz_attempts", None)
    assert fn is not None, "get_quiz_attempts must be defined"

    raw = fn("session_123")
    data = json.loads(raw)
    assert data.get("session_id") == "session_123", "Must include session_id in JSON"
    assert "attempts" in data, "Must include attempts in JSON"

    print(f"✅ MCP Resources check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
