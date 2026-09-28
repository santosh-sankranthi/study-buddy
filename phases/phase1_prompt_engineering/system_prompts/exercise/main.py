"""EXERCISE -- System Prompts: add the FLASHCARD persona.

The demo added TUTOR_SYSTEM_PROMPT and wired it into app/prompts.py.
Your twist: add a second persona — a strict JSON-only flashcard generator —
to the SAME file and verify the app uses it when mode="flashcard".

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat  # noqa: E402

# ── TODO(1): In app/prompts.py, add the following constant ───────────────────
# (Do this in the real file; the check will import from there.)
#
# FLASHCARD_SYSTEM_PROMPT = """You are a flashcard generator.
#
# Rules:
# - Reply ONLY with a valid JSON object in this exact format:
#   {"front": "...", "back": "..."}
# - front: a clear question or prompt.
# - back: a concise answer (1-2 sentences max).
# - No other text, no markdown fences, no explanation.
# """

# ── TODO(2): In app/prompts.py's build_system(), handle mode="flashcard" ─────
# Add:  elif mode == "flashcard":
#           base = FLASHCARD_SYSTEM_PROMPT


# ── TODO(3): Verify your flashcard persona works ──────────────────────────────
# Import the constant you just added and test it below.

from app.prompts import FLASHCARD_SYSTEM_PROMPT  # noqa: E402 — must exist after TODO(1)

topic    = "The Calvin cycle"
response = chat([
    {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
    {"role": "user",   "content": topic},
])

print("Raw response:", response)
print()

# Parse and validate.
card = json.loads(response)  # will raise json.JSONDecodeError if not valid JSON
assert "front" in card, "Missing 'front' key"
assert "back"  in card, "Missing 'back' key"
assert card["front"].strip(), "'front' must not be empty"
assert card["back"].strip(),  "'back' must not be empty"

print("✅  Flashcard generated successfully:")
print(f"   front: {card['front']}")
print(f"   back:  {card['back']}")
