"""Self-check for Phase 3.3 Human Evals rubric."""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    doc = (TARGET / "solution" / "human_eval_rubric.md") if args.solution else (TARGET / "exercise" / "human_eval_rubric.md")
    content = doc.read_text(encoding="utf-8")

    assert "Accuracy" in content, "Missing Accuracy criterion"
    assert "Pedagogical Empathy" in content, "Missing Pedagogical Empathy criterion"
    assert "Socratic Guidance" in content, "Missing Socratic Guidance criterion"

    for i in range(1, 6):
        assert f"Sample {i}" in content, f"Missing Sample {i}"

    if not args.solution:
        assert "TODO" not in content, "Please fill in all scores and rationales in human_eval_rubric.md"

    print(f"✅ Human evals rubric check passed ({doc.name})!")

if __name__ == "__main__":
    main()
