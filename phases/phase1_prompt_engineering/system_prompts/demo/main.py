"""DEMO -- System Prompts.

Live-code target: give Study Buddy a Socratic tutor persona and compare
responses with/without it. Then wire it into app/prompts.py so the running app
uses the persona on every request.

Run standalone:
    python phases/phase1_prompt_engineering/system_prompts/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat  # noqa: E402

QUESTION = "What is photosynthesis?"

# ── Step 1: No system prompt (v0 behaviour) ──────────────────────────────────
print("=" * 60)
print("WITHOUT system prompt (v0 raw):")
print("=" * 60)
answer_raw = chat([{"role": "user", "content": QUESTION}])
print(answer_raw)

# ── Step 2: With tutor persona ────────────────────────────────────────────────
TUTOR_SYSTEM_PROMPT = """You are Study Buddy, a warm and patient Socratic tutor.

Rules:
- Never give the answer directly. Ask ONE guiding question that leads the student toward it.
- Keep every reply under 4 sentences total.
- Always end with a short encouraging phrase (e.g. "You're on the right track!").
"""

print("\n" + "=" * 60)
print("WITH TUTOR_SYSTEM_PROMPT:")
print("=" * 60)
answer_tutor = chat([
    {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
    {"role": "user",   "content": QUESTION},
])
print(answer_tutor)

print("\n── What changed ─────────────────────────────────────────────")
print("  Raw:   Long, encyclopaedic, inconsistent tone.")
print("  Tutor: Short, asks a question, ends encouragingly.")
print()
print("Next: open app/prompts.py and wire TUTOR_SYSTEM_PROMPT")
print("      into the /ask endpoint so every call uses it.")
