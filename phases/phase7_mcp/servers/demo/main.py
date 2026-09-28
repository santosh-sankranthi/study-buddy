"""DEMO -- Exposing Tools via FastMCP Server.

The instructor demonstrates defining and inspecting an MCP server.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from mcp_server.server import mcp_app

print("MCP Server initialized:", getattr(mcp_app, "name", "StudyBuddy"))
if hasattr(mcp_app, "_tool_manager"):
    tools = list(mcp_app._tool_manager._tools.keys())
    print("Registered MCP Tools:", tools)
else:
    print("MCP Server ready to accept client connections over stdio.")
