# ReAct: Reason + Act Pattern

> **Time:** ~3 min read | **Goal:** Understand the Thought → Action → Observation agentic loop.

---

## 1. Why Single-Step Prompts Fall Short

Single-shot LLM queries fail when a task requires:
1. Information not in the model's weights
2. Multiple dependent steps (e.g., look up when the test is, then fetch notes for that subject, then summarize)
3. Self-correction if a search query yields no results

---

## 2. The ReAct Framework

Published by Yao et al. (2022), **ReAct** interleaves reasoning (*Thought*) and domain actions (*Action*):

```
┌────────────────────────────────────────────────────────┐
│                        User Goal                       │
└───────────────────────────┬────────────────────────────┘
                            │
              ┌─────────────▼─────────────┐
              │          Thought          │
              │  "What should I do next?" │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │           Action          │
              │   Call tool with args     │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │        Observation        │
              │  Raw output returned      │
              └─────────────┬─────────────┘
                            │
                   Is goal achieved?
                   ├── No  ──► Loop back to Thought
                   └── Yes ──► FINISH with final answer
```

---

## 3. Human Trace Example

**Goal:** "How many days until my Biology exam, and what chapters should I read?"

1. **Thought:** First, I need to know the date of the Biology exam.
2. **Action:** `get_exam_schedule(subject="Biology")`
3. **Observation:** "Biology exam is scheduled for 2026-11-15."
4. **Thought:** Today is September 28, 2026. The exam is 48 days away. Now I need to search notes for Biology topics.
5. **Action:** `search_notes(query="biology exam key topics")`
6. **Observation:** "Focus on Cell Respiration, Photosynthesis, and Genetics."
7. **Thought:** I have both the exam date and the relevant review topics. I can formulate the final answer.
8. **Action:** `FINISH(answer="Your Biology exam is on November 15, 2026 (48 days away). You should review Cell Respiration, Photosynthesis, and Genetics.")`

In Phase 3, our FastAPI app will execute this entire loop autonomously with real LLM tool calls.
