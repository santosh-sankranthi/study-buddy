# Agent Safety Guardrails: Step Caps & Loop Detection

> **Time:** ~2 min read | **Goal:** Prevent runaway agent loops, runaway API costs, and tool invocation thrashing.

---

## 1. Why Agents Run Away

LLM agents are non-deterministic state machines. Without explicit guards, they can enter infinite loops:
1. **Repeated Action Loop:** The model calls `search_notes(query="bio")`, receives "No notes found", and immediately calls `search_notes(query="bio")` again.
2. **Ping-Pong Loop:** The model oscillates between two tools without making progress.
3. **Runaway Verbosity:** The model takes 50 exploratory steps for a simple 1-step question.

If left unchecked, this burns tokens, drains account credits, and hangs the user interface.

---

## 2. Guardrail 1: Hard Step Limit (`MAX_STEPS`)

Every agent loop must enforce an immutable step limit:
```python
MAX_STEPS = 10
for step in range(MAX_STEPS):
    ...
return {"halted": True, "reason": "max_steps"}
```
If the agent fails to reach `FINISH` within `MAX_STEPS`, execution terminates immediately.

---

## 3. Guardrail 2: Loop Detection

If the agent emits the exact same tool name with the exact same JSON arguments twice in a row:
```python
if current_action == last_action and last_action not in (None, "", "FINISH"):
    return {"halted": True, "reason": "loop_detected"}
```
We halt immediately rather than allowing the model to waste remaining steps repeating identical failed calls.
