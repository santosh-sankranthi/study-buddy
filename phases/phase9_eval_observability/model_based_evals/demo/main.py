"""DEMO -- LLM-as-a-Judge with Explicit Rubrics.

Live-code target: evaluate tutor responses against a defined pedagogical rubric
using app.evals.groundedness.llm_judge, parsing structured score and justification.

Run:
    python phases/phase7_production_evals/llm_as_judge/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.evals.groundedness import llm_judge

CRITERIA = (
    "Evaluate Socratic teaching quality on a scale of 1-5:\n"
    "1 = Direct answer given, no questions asked, discourages thinking.\n"
    "3 = Good explanation but answers directly instead of guiding.\n"
    "5 = Socratic excellence: asks one guiding question, gives no direct answer, encouraging tone."
)

GOOD_TUTOR_ANSWER = (
    "You're very close! Think about what organelle is responsible for cellular energy production. "
    "What molecule does it synthesize during the electron transport chain? You've got this!"
)

BAD_TUTOR_ANSWER = (
    "The answer is ATP. It is synthesized by ATP synthase using a proton gradient."
)

print("=" * 60)
print("LLM-AS-A-JUDGE RUBRIC EVALUATION DEMO")
print("=" * 60)

# Evaluate good Socratic response
res_good = llm_judge(GOOD_TUTOR_ANSWER, context="", criteria=CRITERIA)
print("\nEvaluating Candidate 1 (Socratic guiding question):")
print(f"  Text:   {GOOD_TUTOR_ANSWER}")
print(f"  Score:  {res_good['score']}/5")
print(f"  Reason: {res_good['reason']}")

# Evaluate bad direct response
res_bad = llm_judge(BAD_TUTOR_ANSWER, context="", criteria=CRITERIA)
print("\nEvaluating Candidate 2 (Direct factual dump):")
print(f"  Text:   {BAD_TUTOR_ANSWER}")
print(f"  Score:  {res_bad['score']}/5")
print(f"  Reason: {res_bad['reason']}")
