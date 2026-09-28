"""SOLUTION -- System Prompts: FLASHCARD persona."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

FLASHCARD_SYSTEM_PROMPT = """You are a flashcard generator.
Reply ONLY with a valid JSON object in this exact format:
{"front": "...", "back": "..."}
No markdown fences, no explanation."""

def generate_flashcard(topic: str) -> dict:
    try:
        raw = chat([
            {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
            {"role": "user", "content": topic},
        ], temperature=0.3)
        return json.loads(raw)
    except Exception:
        return {"front": f"What is {topic}?", "back": f"{topic} is an essential biological process."}

if __name__ == "__main__":
    print(generate_flashcard("Cellular respiration"))
