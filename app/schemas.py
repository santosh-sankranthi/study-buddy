"""Pydantic schemas for structured output endpoints.

Grows through the phases:
  Phase 1.4 — Flashcard, StudyPlanDay, QuizItem
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Structured output  [Phase 1.4]
# Pydantic classes that define the exact shape we require from the model. If the
# model's JSON does not match, validation raises instead of silently misbehaving.
# Wired into: /flashcards (Flashcard), /study-plan (StudyPlanDay), /quiz-item (QuizItem).
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator


# ── Phase 1.4 ────────────────────────────────────────────────────────────────

class Flashcard(BaseModel):
    """A single study flashcard with a difficulty rating."""
    question:   str
    answer:     str
    difficulty: Literal["easy", "medium", "hard"]


class StudyPlanDay(BaseModel):
    """One day in a structured study plan."""
    subject: str
    topics:  list[str]
    minutes: int

    @field_validator("topics")
    @classmethod
    def topics_non_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("topics must not be empty")
        if any(not t.strip() for t in v):
            raise ValueError("each topic must be a non-empty string")
        return v

    @field_validator("minutes")
    @classmethod
    def minutes_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("minutes must be a positive integer")
        return v


class QuizItem(BaseModel):
    """A multiple-choice quiz item."""
    question:      str
    options:       list[str]
    correct_index: int

    @field_validator("options")
    @classmethod
    def four_options(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("options must have exactly 4 entries")
        return v

    @field_validator("correct_index")
    @classmethod
    def valid_index(cls, v: int) -> int:
        if not (0 <= v <= 3):
            raise ValueError("correct_index must be 0–3")
        return v
