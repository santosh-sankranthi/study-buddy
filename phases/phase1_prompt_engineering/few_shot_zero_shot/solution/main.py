"""SOLUTION -- Few-Shot / Zero-Shot."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.prompts import build_few_shot_prompt  # noqa: E402
from common.llm import chat  # noqa: E402

MY_EXAMPLES: list[dict] = [
    {"input": "Cellular respiration", "output": "_____ is the organelle that makes ATP.\nAnswer: Mitochondria"},
    {"input": "Newton's first law", "output": "An object at rest stays at rest due to _____.\nAnswer: Inertia"},
]


def messages_for(topic: str) -> list[dict]:
    return build_few_shot_prompt(MY_EXAMPLES, topic)


def generate(topic: str) -> str:
    return chat(messages_for(topic), temperature=0.0)


if __name__ == "__main__":
    print(generate("The Calvin cycle"))
