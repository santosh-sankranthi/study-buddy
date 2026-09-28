# Phase 6 Instructor Guide: AI Agents & Autonomous Loops

## Learning Objectives
1. Wire Python functions into a callable `TOOL_REGISTRY`.
2. Parse model `tool_calls` payloads and dispatch execution.
3. Implement autonomous ReAct loops with visible think/act/observe trace logging.
4. Enforce strict termination guards: `MAX_STEPS` caps and loop detection.
5. Coordinate multi-agent workflows (Planner, Executor, Critic).

## Timing & Pacing (Total: 60 min)
- **6.1 Tools (10 min)**: Wire `search_notes` and `get_exam_schedule`.
- **6.2 Function Calling Live (12 min)**: Dispatch execution of tool calls.
- **6.3 ReAct Loop (15 min)**: Trace execution through multi-step questions.
- **6.4 Agent Loops (13 min)**: Implement same-tool loop detection.
- **6.5 Multi-Agent Systems (10 min)**: Add Critic verification to Planner/Executor.
