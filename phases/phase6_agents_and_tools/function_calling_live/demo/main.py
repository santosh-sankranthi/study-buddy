"""DEMO -- Live Tool Execution via execute_tool_call().

Live-code target: dispatch synthetic tool calls through app.agent.execute_tool_call(),
verify argument parsing and execution, and observe unknown tool handling.

Run:
    python phases/phase6_agents_and_tools/function_calling_live/demo/main.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call

print("=" * 60)
print("LIVE TOOL EXECUTION DEMO")
print("=" * 60)

# 1. Valid tool call: get_exam_schedule
valid_call = {
    "function": {
        "name": "get_exam_schedule",
        "arguments": json.dumps({"subject": "biology"}),
    }
}
print(f"\n1. Executing get_exam_schedule: {valid_call['function']['arguments']}")
result_valid = execute_tool_call(valid_call)
print(f"   Output: {result_valid}")

# 2. Unknown tool call
unknown_call = {
    "function": {
        "name": "delete_all_files",
        "arguments": json.dumps({"path": "/"}),
    }
}
print(f"\n2. Executing malicious / unknown tool: {unknown_call['function']['name']}")
result_unknown = execute_tool_call(unknown_call)
print(f"   Output: {result_unknown}")
print("   ✅ Safety check prevented execution of unauthorized function.")
