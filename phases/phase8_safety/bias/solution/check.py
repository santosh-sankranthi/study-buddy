"""Self-check for Phase 8.3 Bias exercise."""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    doc = (TARGET / "solution" / "bias_observation.md") if args.solution else (TARGET / "exercise" / "bias_observation.md")
    content = doc.read_text(encoding="utf-8")

    assert "Prompt Variation A" in content, "Missing Variation A section"
    assert "Prompt Variation B" in content, "Missing Variation B section"
    assert "Analysis of Differences" in content, "Missing Analysis section"

    if not args.solution:
        assert "TODO" not in content, "Please fill in the TODO observation gaps in bias_observation.md"

    print(f"✅ Bias observation check passed ({doc.name})!")

if __name__ == "__main__":
    main()
