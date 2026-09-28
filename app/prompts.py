"""System prompt constants and helpers used across all phases.

Instructor: this file grows every phase.
  Phase 1.1 — TUTOR_SYSTEM_PROMPT, FLASHCARD_SYSTEM_PROMPT, build_system()
  Phase 1.2 — build_few_shot_prompt()
  Phase 1.3 — CoT injection handled inline in main.py
  Phase 1.4 — schemas live in app/schemas.py
"""

from __future__ import annotations

from datetime import datetime

# ── Phase 1.1 ────────────────────────────────────────────────────────────────

TUTOR_SYSTEM_PROMPT = """You are Study Buddy, a warm and patient Socratic tutor.

Rules:
- Never give the answer directly. Ask ONE guiding question that leads the student toward it.
- Keep every reply under 4 sentences total.
- Always end with a short encouraging phrase (e.g. "You're on the right track!").
- If the student is clearly stuck, give a hint — not the full answer.
"""

FLASHCARD_SYSTEM_PROMPT = """You are a flashcard generator.

Rules:
- Reply ONLY with a valid JSON object in this exact format:
  {"front": "...", "back": "..."}
- front: a clear question or prompt.
- back: a concise answer (1–2 sentences max).
- No other text, no markdown fences, no explanation.
"""

DIRECT_SYSTEM_PROMPT = ""  # No system prompt — raw v0 behaviour.


def build_system(
    mode: str = "tutor",
    student_name: str | None = None,
    study_goal: str | None = None,
    inject_date: bool = True,
) -> str:
    """Assemble the full system prompt from parts.

    Phase 2.1 adds date injection and student-name injection here.
    """
    if mode == "tutor":
        base = TUTOR_SYSTEM_PROMPT
    elif mode == "flashcard":
        base = FLASHCARD_SYSTEM_PROMPT
    else:
        base = ""  # direct / no persona

    prefix_lines: list[str] = []

    if inject_date:
        prefix_lines.append(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.")

    if student_name:
        prefix_lines.append(f"The student's name is {student_name}.")

    if study_goal:
        prefix_lines.append(f"The student's current study goal: {study_goal}.")

    prefix = "\n".join(prefix_lines)
    if prefix and base:
        return prefix + "\n\n" + base
    return prefix or base


# ── Phase 1.2 ────────────────────────────────────────────────────────────────

def build_few_shot_prompt(examples: list[dict], task_input: str) -> list[dict]:
    """Build a few-shot message list from {input, output} dicts.

    Args:
        examples:   List of dicts with keys "input" and "output".
        task_input: The actual user query to append at the end.

    Returns:
        A messages list ready to pass to chat().
    """
    messages: list[dict] = []
    for ex in examples:
        messages.append({"role": "user",      "content": ex["input"]})
        messages.append({"role": "assistant", "content": ex["output"]})
    messages.append({"role": "user", "content": task_input})
    return messages
