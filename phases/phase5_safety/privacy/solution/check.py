"""Self-check for Phase 5.2 Privacy / PII."""
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

    fn = getattr(mod, "scrub_international_phone", None)
    assert fn is not None, "scrub_international_phone must be defined"

    clean, types = fn("Contact me at +91 9876543210 or +44 7911123456")
    assert "PHONE_IN" in types and "PHONE_UK" in types, "Must detect both phone types"
    assert "+91" not in clean and "+44" not in clean, "Phone numbers must be redacted"

    print(f"✅ Privacy check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
