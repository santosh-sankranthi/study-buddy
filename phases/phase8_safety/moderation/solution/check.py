"""Self-check for Phase 8.4 Moderation."""
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

    fn = getattr(mod, "moderate_assistant_output", None)
    assert fn is not None, "moderate_assistant_output must be defined"

    res = fn("Cellular respiration generates ATP in plant and animal cells.")
    assert res.get("status") == "APPROVED", "Safe educational content must be approved"
    assert res.get("flagged") is False

    print(f"✅ Moderation check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
