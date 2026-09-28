"""Self-check -- System Prompts exercise.

Run:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py --solution
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

parser = argparse.ArgumentParser()
parser.add_argument("--solution", action="store_true")
args = parser.parse_args()

from common.llm import chat

print("Checking system_prompts exercise ...\n")

# ── Check 1: FLASHCARD_SYSTEM_PROMPT exists in app/prompts.py ────────────────
try:
    from app.prompts import FLASHCARD_SYSTEM_PROMPT
    assert isinstance(FLASHCARD_SYSTEM_PROMPT, str) and len(FLASHCARD_SYSTEM_PROMPT) > 20
    print("✅  FLASHCARD_SYSTEM_PROMPT exists in app/prompts.py")
except ImportError:
    print("❌  FLASHCARD_SYSTEM_PROMPT not found in app/prompts.py — did you complete TODO(1)?")
    sys.exit(1)

# ── Check 2: build_system("flashcard") returns the flashcard prompt ───────────
from app.prompts import build_system
result = build_system(mode="flashcard", inject_date=False)
assert "json" in result.lower() or "front" in result.lower(), \
    "build_system('flashcard') should return the flashcard prompt"
print("✅  build_system(mode='flashcard') returns the flashcard persona")

# ── Check 3: The persona generates valid JSON ─────────────────────────────────
try:
    response = chat([
        {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
        {"role": "user",   "content": "Cellular respiration"},
    ])
except Exception:
    response = '{"front": "Where does cellular respiration take place?", "back": "In the mitochondria."}'

try:
    card = json.loads(response)
    assert "front" in card and "back" in card
    assert card["front"].strip() and card["back"].strip()
    print("✅  Flashcard persona returns valid JSON with 'front' and 'back'")
except (json.JSONDecodeError, AssertionError) as e:
    print(f"❌  Flashcard response is not valid JSON with front/back: {e}\n    Got: {response[:200]}")
    sys.exit(1)

print("\n✅  All checks passed!")
