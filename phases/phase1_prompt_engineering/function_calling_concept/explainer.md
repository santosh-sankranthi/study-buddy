# Function Calling (Concept Introduction)

> **Time:** ~2 min read | **Goal:** Understand tool schemas and how LLMs request actions without executing them directly.

---

## 1. What is Function Calling?

Language models cannot run Python code, query databases, or fetch real-time web pages on their own. They are pure text generators.

**Function calling** is the standardized protocol where:
1. You describe Python functions to the model using JSON Schema (names, descriptions, parameter types, requirements).
2. The model inspects the user's prompt and decides if calling one or more functions is necessary.
3. Instead of producing free-form natural language, the model emits a structured JSON object specifying:
   - Function name (e.g., `search_notes`)
   - Arguments (e.g., `{"query": "photosynthesis"}`)
4. **Your application** receives this request, executes the actual code safely, and returns the result back to the model.

---

## 2. Key Rule: The Model Decides *What*, You Decide *How*

The model **never** executes code directly. It simply says:
*"I would like you to run `get_exam_schedule(subject='Biology')`."*

This architecture gives you total control:
- Security validation
- Rate limiting
- Authorization & permissions
- Mocking and sandboxing

---

## 3. Tool Schema Anatomy

Every tool in the OpenAI / OpenRouter format consists of:

```json
{
  "type": "function",
  "function": {
    "name": "calculate_grade",
    "description": "Calculates weighted average from score and weight lists",
    "parameters": {
      "type": "object",
      "properties": {
        "scores":  {"type": "array", "items": {"type": "number"}},
        "weights": {"type": "array", "items": {"type": "number"}}
      },
      "required": ["scores", "weights"]
    }
  }
}
```

In Phase 1, we master tool schema design. In Phase 3, we implement full multi-step agentic execution.
