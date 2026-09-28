"""EXERCISE -- Few-Shot: fill-in-the-blank format instead of MCQ.

The demo built an MCQ quiz-item generator with 2 pre-loaded examples.
Your twist: replace the MCQ examples with YOUR OWN 2 examples that
produce a FILL-IN-THE-BLANK style question instead.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt  # noqa: E402

# ── TODO(1): Write 2 fill-in-the-blank examples in the same {input, output} format.
# Each output should contain a blank marker like "___" or "(blank)".
# Example input:  "Mitochondria"
# Example output: "The _____ is the powerhouse of the cell." / (blank: mitochondria)

MY_EXAMPLES: list[dict] = [
    {"input": "Mitochondria", "output": "The _____ is the powerhouse of the cell. (blank: mitochondria)"},
    {"input": "Chloroplast", "output": "Photosynthesis takes place within plant _____ organelles. (blank: chloroplast)"},
]

# ── TODO(2): Call build_few_shot_prompt with your new examples on a new topic.
# Pick a topic different from the demo's "The water cycle".
MY_TOPIC = "Ribosome"


# ── Run your few-shot call ────────────────────────────────────────────────────
if __name__ == "__main__":
    assert MY_EXAMPLES, "TODO(1): MY_EXAMPLES is empty — add your 2 examples first."
    assert MY_TOPIC,    "TODO(2): MY_TOPIC is empty — pick a topic."

    messages = build_few_shot_prompt(MY_EXAMPLES, MY_TOPIC)
    result   = chat(messages, temperature=0.4)

    print("Topic:", MY_TOPIC)
    print("Result:\n", result)

    # Verify the output looks like a fill-in-the-blank item.
    has_blank = "___" in result or "(blank)" in result.lower() or "blank" in result.lower()
    assert has_blank, (
        "Expected a fill-in-the-blank format. "
        "Make sure your examples use '___' or '(blank)' to mark the missing word."
    )
    print("\n✅  Output is in fill-in-the-blank format.")
