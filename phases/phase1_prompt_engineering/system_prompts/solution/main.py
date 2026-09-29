"""SOLUTION -- System Prompts."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat  # noqa: E402

FLASHCARD_SYSTEM_PROMPT = (
    'You are a flashcard generator. Reply ONLY with a JSON object '
    'like {"front": "question", "back": "answer"}. No other text.'
)


def build_messages(topic: str) -> list[dict]:
    return [
        {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
        {"role": "user", "content": topic},
    ]


def generate_flashcard(topic: str) -> dict:
    return json.loads(chat(build_messages(topic), temperature=0.0))


if __name__ == "__main__":
    print(generate_flashcard("Cellular respiration"))
