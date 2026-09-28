"""EXERCISE -- System Prompts: add the FLASHCARD persona.

The demo added TUTOR_SYSTEM_PROMPT.
Your twist: define FLASHCARD_SYSTEM_PROMPT instructing the model to reply ONLY
with valid JSON: {"front": "...", "back": "..."}.

Run when done:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

# TODO(1): Define FLASHCARD_SYSTEM_PROMPT
FLASHCARD_SYSTEM_PROMPT = ""

def generate_flashcard(topic: str) -> dict:
    """Call chat() with FLASHCARD_SYSTEM_PROMPT and return the parsed JSON dict."""
    raise NotImplementedError("TODO(2): implement generate_flashcard")

if __name__ == "__main__":
    print(generate_flashcard("Cellular respiration"))
