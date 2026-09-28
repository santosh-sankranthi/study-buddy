"""EXERCISE -- Flashcard Quality Evaluation with Custom Rubric.

The demo evaluated Socratic tutor persona quality.
Your twist: implement evaluate_flashcard_quality() with a tailored 1-5 rubric
assessing whether the front is a distinct question, the back is a concise fact,
and difficulty matches the cognitive complexity.

Fill in every TODO. Run when done:
    python phases/phase7_production_evals/llm_as_judge/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.evals.groundedness import llm_judge

FLASHCARD_RUBRIC = (
    "Evaluate flashcard quality on a 1-5 scale:\n"
    "1 = Incoherent, reveals answer on front, or rambling text.\n"
    "3 = Functional question and answer, but ambiguous wording or too verbose.\n"
    "5 = Atomic, clear conceptual question on front; concise, accurate definition on back."
)


# ── TODO(1): Implement evaluate_flashcard_quality ────────────────────────────
def evaluate_flashcard_quality(
    question: str,
    answer: str,
    difficulty: str,
    rubric: str = FLASHCARD_RUBRIC,
) -> dict:
    """Evaluate flashcard using llm_judge.

    Returns {"score": int (1-5), "reason": str}.
    """
    card_text = f"Question: {question}\nAnswer: {answer}\nDifficulty: {difficulty}"
    # TODO(1): return llm_judge(card_text, context="", criteria=rubric)
    return llm_judge(card_text, context="", criteria=rubric)


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Explicit rubrics with concrete anchor examples anchor model judges, "
    "reducing variance and preventing score inflation on nuanced qualitative evaluations."
)


if __name__ == "__main__":
    q = "What is the primary function of chloroplasts in plant cells?"
    a = "To conduct photosynthesis and produce glucose."
    d = "easy"
    eval_result = evaluate_flashcard_quality(q, a, d)
    print("Flashcard Evaluation Result:")
    print(f"  Score:  {eval_result['score']}/5")
    print(f"  Reason: {eval_result['reason']}")
    print("\nObservation:", OBSERVATION)
