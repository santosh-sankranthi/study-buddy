"""SOLUTION -- Add calculate_grade to MCP Server."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade
from mcp_server.server import mcp_app

def register_grade_tool(server) -> bool:
    if hasattr(server, "tool"):
        server.tool()(calculate_grade)
        return True
    return False

if __name__ == "__main__":
    print("Registration status:", register_grade_tool(mcp_app))
