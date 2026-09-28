# The Autonomous ReAct Loop

> **Time:** ~2 min read | **Goal:** Build the autonomous Thought → Action → Observation execution cycle that powers real AI agents.

---

## 1. Single Tool vs. Agentic Loop

- **Single Tool Call:** A model is asked a question, decides to invoke one tool, gets the result, and outputs an answer. (Linear, 1-step).
- **Agentic Loop:** The model can call Tool A, examine the result, decide that the result requires calling Tool B, observe the second result, and only then synthesize a comprehensive answer.

---

## 2. The Execution State Machine

```
User Prompt
     │
     ▼
┌──────────────┐
│  Call Model  │◄───────────────────────────┐
└──────┬───────┘                            │
       │                                    │
       ├─ Has tool_calls? ──► [Execute Tool] │
       │                      [Append result]
       ▼
  Done (finish_reason == "stop")
       │
       ▼
 Final Answer
```

At every cycle:
1. `messages` grows with:
   - The assistant's `tool_calls` request
   - The environment's `role: "tool"` response
2. The agent maintains working memory of everything discovered in earlier iterations.
