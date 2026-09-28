"""EXERCISE -- Call calculate_grade through MCP Client.

The demo listed MCP tools.
Your twist: execute calculate_grade through the MCP protocol end-to-end.

Run when done:
    python phases/phase4_mcp/clients/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import call_mcp_tool

# TODO(1): Call call_mcp_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]})
#   Store the result in `grade_result` and print it.

grade_result = ""


if __name__ == "__main__":
    # TODO(2): Uncomment and run once implemented:
    # assert grade_result != "", "TODO: assign grade_result"
    print("MCP grade result:", grade_result)
