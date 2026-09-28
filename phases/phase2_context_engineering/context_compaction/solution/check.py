"""Self-check for Phase 2.3 Compaction."""
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

    fn = getattr(mod, "compact_keep_last2", None)
    assert fn is not None, "compact_keep_last2 function must be defined"

    conv = mod.setup_test_conversation("test_sid")
    compacted = fn(conv)
    assert len(compacted) == 3, f"Expected 3 items (summary + last 2), got {len(compacted)}"
    assert "[SUMMARY]" in compacted[0]["content"], "First message must be summary"

    print(f"✅ Context compaction check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
