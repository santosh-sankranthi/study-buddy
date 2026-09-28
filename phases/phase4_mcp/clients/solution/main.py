"""SOLUTION -- Call calculate_grade through MCP Client."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import call_mcp_tool

grade_result = call_mcp_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]})

if __name__ == "__main__":
    print("MCP grade result:", grade_result)
