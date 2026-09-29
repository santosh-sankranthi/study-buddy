"""EXERCISE -- ReAct loop: one think -> act -> observe turn.

Practice: each turn appends the model's tool call and the tool's real result.

Task: finish apply_tool_call() so it returns the grown message list.

Check your work with:
    python phases/phase3_agents_and_tools/react_loop/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call

MESSAGES = [{"role": "user", "content": "When is the biology exam?"}]
TOOL_CALL = {"id": "call_1", "type": "function",
             "function": {"name": "get_exam_schedule", "arguments": '{"subject": "biology"}'}}


def apply_tool_call(messages: list[dict], tool_call: dict) -> list[dict]:
    """Return `messages` plus the assistant tool call and the tool result."""
    # TODO(1): observation = execute_tool_call(tool_call)
    # TODO(2): append {"role": "assistant", "content": None, "tool_calls": [tool_call]}
    #          then {"role": "tool", "content": observation, "tool_call_id": tool_call["id"]}
    raise NotImplementedError("apply_tool_call")


if __name__ == "__main__":
    for message in apply_tool_call(MESSAGES, TOOL_CALL):
        print(message)
