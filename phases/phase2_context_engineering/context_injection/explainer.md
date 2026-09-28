# Context Sources & Metadata Injection

> **Time:** ~2 min read | **Goal:** Understand where context originates, how to account for it, and how metadata injection enhances prompt relevance.

---

## 1. What is Context?

Context is not just the user's latest question. In a production AI application, a single request payload sent to the LLM typically combines:
1. **System Persona & Constraints:** Base instructions that define behavior and safety guards.
2. **Dynamic Metadata:** Today's date, student name, grade level, enrolled subjects.
3. **Session History:** Previous turns between the user and assistant.
4. **Retrieved Context (RAG):** Relevant knowledge base chunks.
5. **Tool Output:** Raw execution returns from functions or APIs.
6. **User Input:** The current user query.

All of these compete for the same **finite context window**.

---

## 2. Context Accounting

To prevent silent truncation or API limit exceptions, we must track token consumption by category:
- `system`: Base prompt + injected metadata
- `user`: User questions and injected documents
- `assistant`: Past model responses
- `total`: The aggregate context load

`app/context.py` provides `context_report(messages)` to compute these breakdowns on every request.

---

## 3. Dynamic Metadata Injection

Instead of hardcoding details, the application dynamically constructs the system prompt:
```python
system_content = f"Today is {current_date}.\nThe student's name is {student_name}.\n{BASE_SYSTEM_PROMPT}"
```
This enables personalized responses (addressing the student by name) and temporal awareness (knowing what day it is) without retraining the model.
