# Live Tool Execution & Dispatch

> **Time:** ~2 min read | **Goal:** Bridge the gap between the LLM's requested tool calls and real Python code execution.

---

## 1. From JSON to Python

In Phase 1, we introduced tool schemas. When an LLM decides to invoke a tool, it outputs a `tool_calls` payload:

```json
{
  "id": "call_abc123",
  "type": "function",
  "function": {
    "name": "calculate_grade",
    "arguments": "{\"scores\": [85, 90], \"weights\": [0.5, 0.5]}"
  }
}
```

The model **cannot** run this code. Your backend must:
1. Parse `function.arguments` with `json.loads()`.
2. Look up `function.name` in a trusted dictionary (`TOOL_REGISTRY`).
3. Call the Python function with the unpacked keyword arguments (`fn(**args)`).
4. Catch exceptions safely (e.g. invalid arguments or network errors) so the app doesn't crash.
5. Return the stringified result back to the model as a `role: "tool"` message.

---

## 2. The Tool Dispatcher (`app/agent.py`)

```python
def execute_tool_call(tool_call: dict) -> str:
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        return f"Error: unknown tool {name!r}"
    return str(fn(**args))
```

This guarantees safety: only functions explicitly listed in `TOOL_REGISTRY` can ever be executed.
