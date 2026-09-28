# 3.1 — Tools (Execution-Wired)

## What was broken before
In Phase 1.5, we wrote tool schemas (`TOOLS`), but they were just JSON blueprints. If an LLM decided to call `search_notes` or `calculate_grade`, our app had no code to actually run them!

## How it works
We build a `TOOL_REGISTRY` — a Python dictionary mapping function names (`str`) to callable Python functions. When the model requests a tool call, we look up the name in the registry and execute it with the provided arguments.
