"""EXERCISE -- System Prompts.

Practice: a system message fixes the model's role and output format.

Task: write FLASHCARD_SYSTEM_PROMPT and build_messages().

Check your work with:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
"""

FLASHCARD_SYSTEM_PROMPT = ""  # TODO(1): reply ONLY with JSON {"front": ..., "back": ...}


def build_messages(topic: str) -> list[dict]:
    """Return the [system, user] messages for one flashcard."""
    # TODO(2): system message = the prompt; user message = topic.
    raise NotImplementedError("build_messages")


if __name__ == "__main__":
    print(build_messages("Cellular respiration"))
