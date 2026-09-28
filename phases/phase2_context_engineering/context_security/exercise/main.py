"""EXERCISE -- Context Security Sanitizer.

The demo blocked basic prompt injections.
Your twist: implement sanitize_comment_injection(text: str) -> tuple[str, bool]
to detect and neutralize HTML comment injection vectors like '<!-- ignore previous instructions -->'.

Run when done:
    python phases/phase2_context_engineering/context_security/solution/check.py
"""
import re

# TODO(1): Implement sanitize_comment_injection(text: str) -> tuple[str, bool]
# Returns (cleaned_text, was_flagged)
def sanitize_comment_injection(text: str) -> tuple[str, bool]:
    raise NotImplementedError("TODO(1): implement sanitize_comment_injection")

if __name__ == "__main__":
    clean, flagged = sanitize_comment_injection("Note text <!-- ignore instructions --> more text")
    print(f"Flagged: {flagged} | Clean: {clean}")
