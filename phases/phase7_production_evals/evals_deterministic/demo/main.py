"""DEMO -- Deterministic Evaluation Suite.

Live-code target: run zero-cost deterministic assertions over model outputs,
checking JSON validity, schema compliance, length bounds, and banned phrases.

Run:
    python phases/phase7_production_evals/evals_deterministic/demo/main.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

CANDIDATES = [
    # 1. Perfect output
    '{"question": "What is ATP?", "answer": "The primary energy currency of cells.", "difficulty": "easy"}',
    # 2. Markdown fenced JSON (violates "no fences" rule)
    '```json\n{"question": "What is ATP?", "answer": "Energy molecule.", "difficulty": "easy"}\n```',
    # 3. Invalid enum value
    '{"question": "What is ATP?", "answer": "Energy.", "difficulty": "super_hard"}',
]

BANNED_SUBSTRINGS = ["```", "as an ai", "here is your"]


def evaluate_output(text: str) -> dict[str, bool]:
    has_banned = any(b in text.lower() for b in BANNED_SUBSTRINGS)
    is_valid_json = False
    valid_schema = False

    try:
        data = json.loads(text)
        is_valid_json = True
        if (
            isinstance(data, dict)
            and "question" in data
            and "answer" in data
            and data.get("difficulty") in {"easy", "medium", "hard"}
        ):
            valid_schema = True
    except Exception:
        pass

    return {
        "no_banned_tokens": not has_banned,
        "valid_json": is_valid_json,
        "valid_schema": valid_schema,
        "all_passed": (not has_banned) and is_valid_json and valid_schema,
    }


print("=" * 60)
print("DETERMINISTIC EVALUATION DEMO")
print("=" * 60)

for i, cand in enumerate(CANDIDATES, 1):
    res = evaluate_output(cand)
    status = "✅ PASS" if res["all_passed"] else "❌ FAIL"
    print(f"\nCandidate {i}: {status}")
    print(f"  Input:    {cand[:60]}...")
    print(f"  Checks:   {res}")
