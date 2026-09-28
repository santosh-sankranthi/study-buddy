"""EXERCISE -- LLM-as-a-Judge Tone & Helpfulness.

The demo judged groundedness.
Your twist: define TONE_CRITERIA and implement evaluate_tone(answer: str) -> dict
to score responses on encouragement and clarity on a 1-5 scale.

Run when done:
    python phases/phase9_eval_observability/model_based_evals/solution/check.py
"""
# TODO(1): Define TONE_CRITERIA string
TONE_CRITERIA = ""

# TODO(2): Implement evaluate_tone(answer: str) -> dict
# Return {"score": int (1-5), "reason": str}
def evaluate_tone(answer: str) -> dict:
    raise NotImplementedError("TODO(2): implement evaluate_tone")

if __name__ == "__main__":
    print(evaluate_tone("Great question! Let's think about photosynthesis step by step."))
