"""DEMO -- Structured Output.

Live-code target: define a Pydantic Flashcard schema, call the LLM, validate
the response with model_validate_json(), then deliberately break the schema
to show the validator catching it. Finally wire /flashcards into app/main.py.

Run:
    python phases/phase1_prompt_engineering/structured_output/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.schemas import Flashcard  # defined in Phase 1.4

TOPIC = "Cellular respiration"

SYSTEM = (
    "Return ONLY a valid JSON object matching this schema:\n"
    '{"question": "str", "answer": "str", "difficulty": "easy"|"medium"|"hard"}\n'
    "No markdown fences, no extra text."
)

# ── Step 1: Generate and validate ─────────────────────────────────────────────
print("=" * 60)
print(f"Topic: {TOPIC!r}")
print("=" * 60)
raw = chat([
    {"role": "system", "content": SYSTEM},
    {"role": "user",   "content": f"Make a flashcard for: {TOPIC}"},
], temperature=0.3)

print("Raw model output:")
print(raw)
print()

card = Flashcard.model_validate_json(raw)
print("Validated Flashcard:")
print(f"  question:   {card.question}")
print(f"  answer:     {card.answer}")
print(f"  difficulty: {card.difficulty}")

# ── Step 2: Deliberately break it ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("Deliberately invalid JSON:")
print("=" * 60)
bad_json = '{"question": "What is ATP?", "answer": "Energy carrier", "difficulty": "IMPOSSIBLE"}'
print("Input:", bad_json)
try:
    Flashcard.model_validate_json(bad_json)
except Exception as e:
    print(f"ValidationError (expected): {e}")
    print("✅  Pydantic caught the bad 'difficulty' value before it reached the app.")

print()
print("Next: open app/main.py and add the /flashcards endpoint using")
print("      the Flashcard schema and model_validate_json().")
