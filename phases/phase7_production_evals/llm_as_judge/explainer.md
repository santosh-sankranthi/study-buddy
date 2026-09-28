# LLM-as-a-Judge: Qualitative Evaluation & Rubrics

> **Time:** ~2 min read | **Goal:** Measure subtle, qualitative attributes like pedagogical tone, clarity, and helpfulness using structured model judges.

---

## 1. When Deterministic Checks Aren't Enough

Deterministic checks verify syntax, schemas, and word counts. But they cannot answer:
- *"Was the tutor's tone warm and Socratic, or patronizing?"*
- *"Did the explanation simplify a difficult concept without dumbing it down?"*
- *"Is the suggested flashcard actually useful for studying?"*

For qualitative attributes, we use **LLM-as-a-Judge**.

---

## 2. Designing an Unambiguous Rubric

A common pitfall with LLM judges is asking: *"Rate this 1 to 5."* Without a detailed rubric, judge models drift wildly and suffer from score compression (giving everything a 4 or 5).

A production rubric defines **exact anchors** for each numeric rating:
- **Score 1:** Direct answer given, no questions asked, condescending or robotic tone.
- **Score 3:** Partially guiding, but provides key answers too early or is overly wordy (>5 sentences).
- **Score 5:** Masterful Socratic guidance; asks one targeted question leading the student to deduce the answer; under 4 sentences; ends with encouraging words.

---

## 3. Structured Judge Responses

The judge must return typed JSON containing both the numeric score and the chain-of-thought justification:
```json
{
  "score": 5,
  "reason": "The tutor asked a guided question about ATP synthase without giving away the electron gradient mechanism, maintaining patient encouragement."
}
```
Logging the `reason` field is vital for debugging prompt improvements.
