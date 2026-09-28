"""EXERCISE -- Add calculate_grade to MCP Server.

The demo exposed search_notes and get_exam_schedule as MCP tools.
Your twist: register calculate_grade in the MCP server so clients can
calculate weighted averages over the standard protocol.

Run when done:
    python phases/phase7_mcp/servers/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): In mcp_server/server.py (or implement below):
#   Import calculate_grade from app.tools
#   Expose it with @mcp_app.tool()

def register_grade_tool(server) -> bool:
    """Register calculate_grade with server and return True if successful."""
    raise NotImplementedError("TODO(1): register calculate_grade on the MCP server")


if __name__ == "__main__":
    from mcp_server.server import mcp_app
    print("Registration status:", register_grade_tool(mcp_app))
