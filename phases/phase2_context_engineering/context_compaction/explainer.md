# Context Compaction

> **Time:** ~2 min read | **Goal:** Understand how summarization compaction compresses long histories without losing key facts.

---

## 1. Trimming vs. Compaction

When a conversation history grows too large:
- **Trimming (Sliding Window):** Drops older messages completely. This causes conversational *amnesia* — the user's initial instructions, goals, and corrections are lost.
- **Compaction (Summarization):** Takes older messages, runs a fast summarization prompt, and replaces those messages with a single `[SUMMARY]` system message.

---

## 2. How Compaction Works

```
Original History (12 messages, ~4,000 tokens):
  Turn 1: user: "I want to study for AP Chem. Focus on acids and bases."
  Turn 1: assistant: "Understood! Let's start with pH calculations."
  ...
  Turn 6: user: "What was the formula for Ka again?"

Compacted History (3 messages, ~400 tokens):
  [SUMMARY OF EARLIER TURNS]: "Student is preparing for AP Chem with focus on acids/bases. Reviewed pH calculations and buffer solutions."
  Turn 6: user: "What was the formula for Ka again?"
```

---

## 3. Compaction Strategies

1. **Halving (`compact_if_needed`):** Summarizes the oldest 50% of messages when total tokens exceed a threshold.
2. **Keep-Last-N (`compact_keep_last2`):** Summarizes everything except the most recent N turns, ensuring immediate conversational rhythm remains completely verbatim.
