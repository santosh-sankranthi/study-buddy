"""DEMO -- Multimodal Message Payload Construction.

Live-code target: construct OpenAI/OpenRouter compliant multimodal message payloads
containing mixed text and image_url objects for diagram ingestion.

Run:
    python phases/phase9_advanced_capstone/multimodal/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# 1x1 transparent PNG data URL for demonstration
SAMPLE_PNG_DATA_URI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

PROMPT_TEXT = "Describe this diagram of cellular respiration and extract all labeled enzymes."


def build_multimodal_message(prompt: str, image_uri: str) -> dict:
    """Build an API-compliant multimodal user message."""
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_uri}},
        ],
    }


print("=" * 60)
print("MULTIMODAL PAYLOAD DEMO")
print("=" * 60)

msg = build_multimodal_message(PROMPT_TEXT, SAMPLE_PNG_DATA_URI)
print("\nGenerated Multimodal User Message:")
print(f"Role: {msg['role']}")
print(f"Content parts: {len(msg['content'])}")
print(f"  Part 1 (type={msg['content'][0]['type']}): {msg['content'][0]['text']}")
print(f"  Part 2 (type={msg['content'][1]['type']}): {msg['content'][1]['image_url']['url'][:40]}...")
