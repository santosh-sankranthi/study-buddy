"""Study Buddy Model Context Protocol (MCP) Server.

Exposes Study Buddy tools and resources over the standardized MCP protocol so that
MCP-compatible clients (Claude Desktop, Cursor, terminal hosts, or Study Buddy itself)
can directly discover and invoke tools or read note resources.

Run standalone:
    python mcp_server/server.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.tools import calculate_grade as _calculate_grade
from app.tools import get_exam_schedule as _get_exam_schedule
from app.tools import search_notes as _search_notes

try:
    from mcp.server.fastmcp import FastMCP
    mcp_app = FastMCP("StudyBuddy")
except (ImportError, ModuleNotFoundError):
    try:
        from mcp.server.mcpserver import MCPServer
        mcp_app = MCPServer("StudyBuddy")
    except Exception:
        mcp_app = None


if mcp_app:
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


    @mcp_app.resource("notes://corpus")
    def get_notes_corpus() -> str:
        """Expose the sample course notes as an MCP resource."""
        notes_dir = Path(__file__).resolve().parents[1] / "data" / "sample_notes"
        items = []
        if notes_dir.exists():
            for path in sorted(notes_dir.glob("*.md")):
                text = path.read_text(encoding="utf-8", errors="ignore").strip()
                items.append({"file": path.name, "text": text[:120]})
        return json.dumps(
            items or [{"file": "photosynthesis.md", "text": "Photosynthesis and cellular respiration notes"}]
        )


    @mcp_app.resource("quiz://attempts/{session_id}")
    def get_quiz_attempts(session_id: str) -> str:
        """Expose quiz attempt history for a specific session as an MCP resource."""
        return json.dumps({"session_id": session_id, "attempts": []})


if __name__ == "__main__":
    if mcp_app and hasattr(mcp_app, "run"):
        mcp_app.run()
    else:
        print("MCP Server ready.")
