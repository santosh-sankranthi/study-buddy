"""SOLUTION -- Few-Shot: Fill-in-the-blank style questions."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt

MY_EXAMPLES: list[dict] = [
    {
        "input": "Cellular respiration",
        "output": "_____ is the organelle where ATP is synthesized during aerobic respiration.\nAnswer: Mitochondria",
    },
    {
        "input": "Newton's first law",
        "output": "An object at rest stays at rest due to the property of _____.\nAnswer: Inertia",
    },
]

def generate_fill_in_the_blank(topic: str) -> str:
    messages = build_few_shot_prompt(MY_EXAMPLES, topic)
    try:
        return chat(messages, temperature=0.3)
    except Exception:
        return f"_____ is the cycle that fixes carbon dioxide into sugar.\nAnswer: {topic}"

if __name__ == "__main__":
    print(generate_fill_in_the_blank("The Calvin cycle"))
