# Multi-Agent Workflows: Planner, Executor, Critic

> **Time:** ~2 min read | **Goal:** Deconstruct complex open-ended tasks into modular, cooperating agent roles.

---

## 1. The Monolithic Agent Trap

When a single agent tries to solve a complex multi-stage problem (e.g. *"Create a 2-week exam prep schedule for Math and Biology with chapter summaries and quiz checkpoints"*), it suffers from:
- **Context clutter:** History gets clogged with intermediate tool queries.
- **Goal drift:** The agent forgets earlier sub-tasks while deep in a later sub-task.
- **Premature completion:** The agent assumes a quick partial answer is sufficient.

---

## 2. The Plan-and-Solve Pattern

To tackle high-complexity tasks, we decompose the agent into distinct specialized agents:

```
[User Goal]
     │
     ▼
[1. Planner Agent]   ────► Emits discrete ordered sub-tasks: [Step 1, Step 2, ...]
     │
     ▼
For each step:
     │
     ├─► [2. Executor Agent] ──► Runs tools and generates a candidate answer
     │            ▲
     │            │ (retry if rejected)
     ▼            │
     ├─► [3. Critic Agent]   ──► Asserts quality: {"approved": bool, "reason": str}
     │
     ▼
[Synthesizer]        ────► Combines validated step outputs into the final response
```

---

## 3. Benefits of Role Specialization

1. **Clean Contexts:** The executor only sees the current sub-task, not the entire conversation history.
2. **Quality Gates:** The critic prevents hallucinated or incomplete answers from progressing downstream.
3. **Observability:** If a step fails, you immediately know which step failed and why the critic rejected it.
