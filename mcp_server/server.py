"""Study Buddy Model Context Protocol (MCP) Server.

Exposes Study Buddy tools over the standardized MCP protocol so that
MCP-compatible clients (Claude Desktop, cursor, terminal hosts) can
directly leverage the application's knowledge and calculations.

Run standalone:
    python mcp_server/server.py
"""

import sys
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.tools import calculate_grade as _calculate_grade
from app.tools import get_exam_schedule as _get_exam_schedule
from app.tools import search_notes as _search_notes

try:
    from mcp.server.mcpserver import MCPServer
    mcp_app = MCPServer("StudyBuddy")
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP
    mcp_app = FastMCP("StudyBuddy")


@mcp_app.tool()
def search_notes(query: str) -> str:
    """Search the student's indexed course notes for relevant concepts."""
    return _search_notes(query)


@mcp_app.tool()
def get_exam_schedule(subject: str) -> str:
    """Look up when the exam is scheduled for a given academic subject."""
    return _get_exam_schedule(subject)


@mcp_app.tool()
def calculate_grade(scores: list[float], weights: list[float]) -> str:
    """Calculate the weighted average grade from score and weight lists."""
    return _calculate_grade(scores, weights)


if __name__ == "__main__":
    # Run over stdio transport
    mcp_app.run()
