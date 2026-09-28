"""Self-check for Phase 3.6 Production Monitoring alert rules."""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    doc = (TARGET / "solution" / "alert_rules.md") if args.solution else (TARGET / "exercise" / "alert_rules.md")
    content = doc.read_text(encoding="utf-8")

    alert_count = content.count("Alert:")
    thresh_count = content.count("Threshold:")
    why_count = content.count("Why:")

    assert alert_count >= 3, f"Expected at least 3 Alert: definitions, found {alert_count}"
    assert thresh_count >= 3, f"Expected at least 3 Threshold: definitions, found {thresh_count}"
    assert why_count >= 3, f"Expected at least 3 Why: explanations, found {why_count}"

    if not args.solution:
        assert "TODO" not in content, "Please complete all alert rules in alert_rules.md"

    print(f"✅ Production monitoring check passed ({doc.name})!")

if __name__ == "__main__":
    main()
