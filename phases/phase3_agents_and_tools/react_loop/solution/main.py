"""SOLUTION -- ReAct loop: one think -> act -> observe turn."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call

MESSAGES = [{"role": "user", "content": "When is the biology exam?"}]
TOOL_CALL = {"id": "call_1", "type": "function",
             "function": {"name": "get_exam_schedule", "arguments": '{"subject": "biology"}'}}


def apply_tool_call(messages: list[dict], tool_call: dict) -> list[dict]:
    """Return `messages` plus the assistant tool call and the tool result."""
    observation = execute_tool_call(tool_call)
    assistant = {"role": "assistant", "content": None, "tool_calls": [tool_call]}
    tool = {"role": "tool", "content": observation, "tool_call_id": tool_call["id"]}
    return messages + [assistant, tool]


if __name__ == "__main__":
    for message in apply_tool_call(MESSAGES, TOOL_CALL):
        print(message)
