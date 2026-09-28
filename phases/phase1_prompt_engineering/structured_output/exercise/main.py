"""EXERCISE -- Structured Output with Pydantic.

The demo generated and validated a Flashcard using Pydantic.
Your twist: generate a 3-day StudyPlanDay schedule, validate each day with
StudyPlanDay.model_validate_json() (or TypeAdapter), and ensure Pydantic catches
an invalid plan where minutes is negative or topics is empty.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.schemas import StudyPlanDay

PROMPT = (
    "Generate a 3-day study plan for introductory Biology. "
    "Return ONLY a JSON array of objects. "
    'Each object must have: "subject" (str), "topics" (list of non-empty str), "minutes" (positive int). '
    "No markdown fences, no conversational text."
)

# ── TODO(1): Call chat() to get the JSON string ──────────────────────────────
def generate_raw_plan() -> str:
    """Call chat() with the prompt above and return the raw string response."""
    # TODO(1): return chat([{"role": "user", "content": PROMPT}], temperature=0.2)
    return chat([{"role": "user", "content": PROMPT}], temperature=0.2)


# ── TODO(2): Parse and validate each day into a list of StudyPlanDay ──────────
def parse_and_validate_plan(raw_json: str) -> list[StudyPlanDay]:
    """Parse raw_json into a list of StudyPlanDay instances."""
    data = json.loads(raw_json)
    # TODO(2): validate each item using StudyPlanDay.model_validate(item)
    return [StudyPlanDay.model_validate(item) for item in data]


# ── TODO(3): Test that Pydantic rejects an invalid day (negative minutes) ─────
def verify_catches_invalid() -> bool:
    """Return True if StudyPlanDay catches an invalid day with negative minutes."""
    bad_item = {"subject": "Math", "topics": ["Algebra"], "minutes": -30}
    try:
        # TODO(3): validate bad_item with StudyPlanDay.model_validate(bad_item)
        StudyPlanDay.model_validate(bad_item)
        return False
    except Exception:
        return True


if __name__ == "__main__":
    print("Generating study plan...")
    raw = generate_raw_plan()
    print("Raw output:\n", raw)
    plan = parse_and_validate_plan(raw)
    print(f"\nSuccessfully validated {len(plan)} days:")
    for d in plan:
        print(f"  {d.subject}: {d.topics} ({d.minutes} mins)")
    print("\nTesting validator on invalid input:")
    caught = verify_catches_invalid()
    print("Caught bad input correctly:", caught)
