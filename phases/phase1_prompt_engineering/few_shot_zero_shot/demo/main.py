"""DEMO -- Few-Shot / Zero-Shot.

Live-code target: build a quiz-item generator using build_few_shot_prompt(),
show how 2 examples reliably produce a multiple-choice item, then wire the
/quiz-item endpoint into app/main.py.

Run:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt  # wired in Phase 1.1

# ── Two MCQ examples ─────────────────────────────────────────────────────────
QUIZ_EXAMPLES = [
    {
        "input":  "Photosynthesis",
        "output": (
            "Q: Where does photosynthesis occur?\n"
            "A) Mitochondria\n"
            "B) Chloroplast ✓\n"
            "C) Nucleus\n"
            "D) Ribosome"
        ),
    },
    {
        "input":  "Newton's first law",
        "output": (
            "Q: What does Newton's first law state?\n"
            "A) F = ma\n"
            "B) Objects in motion stay in motion unless acted on ✓\n"
            "C) Every action has an equal reaction\n"
            "D) Gravity attracts masses"
        ),
    },
]

TOPIC = "The water cycle"

# ── Zero-shot first, to show the baseline ────────────────────────────────────
print("=" * 60)
print("ZERO-SHOT (no examples):")
print("=" * 60)
zero_shot_answer = chat([
    {"role": "system", "content": "Generate one multiple-choice quiz question about the given topic."},
    {"role": "user",   "content": TOPIC},
])
print(zero_shot_answer)

# ── Few-shot with build_few_shot_prompt() ─────────────────────────────────────
print("\n" + "=" * 60)
print("FEW-SHOT (2 examples via build_few_shot_prompt):")
print("=" * 60)
messages     = build_few_shot_prompt(QUIZ_EXAMPLES, TOPIC)
few_shot_ans = chat(messages, temperature=0.4)
print(few_shot_ans)

print("\n── What changed ─────────────────────────────────────────────")
print("  Zero-shot: format varies, may not have 4 options or a checkmark.")
print("  Few-shot:  reliably mirrors the pattern from the examples.")
print()
print("Next: open app/main.py and add the /quiz-item endpoint using")
print("      build_few_shot_prompt(QUIZ_EXAMPLES, topic).")
