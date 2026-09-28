"""DEMO -- Listing Tools via MCP Client."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import list_mcp_tools

tools = list_mcp_tools()
print(f"Connected to MCP Server. Found {len(tools)} tools:")
for t in tools:
    name = t.get("name") if isinstance(t, dict) else getattr(t, "name", str(t))
    print("  •", name)
