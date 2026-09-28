"""EXERCISE -- Deterministic QuizItem Evaluator.

The demo evaluated Flashcards.
Your twist: implement eval_quiz_item_deterministic() to rigorously validate
generated QuizItem outputs (question, 4 options, valid correct_index 0..3, no markdown fences).

Fill in every TODO. Run when done:
    python phases/phase7_production_evals/evals_deterministic/solution/check.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


# ── TODO(1): Implement eval_quiz_item_deterministic ──────────────────────────
def eval_quiz_item_deterministic(raw_text: str) -> dict[str, bool]:
    """Evaluate whether raw_text is a strictly conforming QuizItem JSON.

    Returns:
        {
            "no_fences": bool,
            "valid_json": bool,
            "has_question": bool,
            "has_4_options": bool,
            "valid_correct_index": bool,
            "all_passed": bool,
        }
    """
    no_fences = "```" not in raw_text
    valid_json = False
    has_question = False
    has_4_opts = False
    valid_idx = False

    try:
        data = json.loads(raw_text)
        valid_json = True
        if isinstance(data, dict):
            has_question = bool(data.get("question", "").strip())
            opts = data.get("options")
            has_4_opts = isinstance(opts, list) and len(opts) == 4 and all(isinstance(o, str) and o.strip() for o in opts)
            c_idx = data.get("correct_index")
            valid_idx = isinstance(c_idx, int) and (0 <= c_idx <= 3)
    except Exception:
        pass

    all_passed = no_fences and valid_json and has_question and has_4_opts and valid_idx

    return {
        "no_fences": no_fences,
        "valid_json": valid_json,
        "has_question": has_question,
        "has_4_options": has_4_opts,
        "valid_correct_index": valid_idx,
        "all_passed": all_passed,
    }


if __name__ == "__main__":
    valid_sample = '{"question": "Where does photosynthesis occur?", "options": ["Mitochondria", "Chloroplast", "Nucleus", "Ribosome"], "correct_index": 1}'
    print("Valid sample eval:", eval_quiz_item_deterministic(valid_sample))

    fenced_sample = f"```json\n{valid_sample}\n```"
    print("Fenced sample eval:", eval_quiz_item_deterministic(fenced_sample))
