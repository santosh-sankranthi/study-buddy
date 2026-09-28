"""Study Buddy MCP Client.

Allows Study Buddy to discover and invoke tools served by any MCP server
(such as the Study Buddy MCP server in mcp_server/server.py).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    HAS_MCP = True
except (ImportError, ModuleNotFoundError):
    HAS_MCP = False


async def _list_tools_async() -> list[dict]:
    if not HAS_MCP:
        from app.tools import TOOLS
        return [t["function"] for t in TOOLS]
    server_script = str(Path(__file__).resolve().parents[1] / "mcp_server" / "server.py")
    server_params = StdioServerParameters(command=sys.executable, args=[server_script])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            return [t.model_dump() for t in result.tools]


async def _call_tool_async(name: str, args: dict) -> str:
    if not HAS_MCP:
        from app.tools import TOOL_REGISTRY
        fn = TOOL_REGISTRY.get(name)
        return str(fn(**args)) if fn else f"Unknown tool: {name}"
    server_script = str(Path(__file__).resolve().parents[1] / "mcp_server" / "server.py")
    server_params = StdioServerParameters(command=sys.executable, args=[server_script])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, args)
            return result.content[0].text if result.content else ""


def list_mcp_tools() -> list[dict]:
    """List tools exposed by the MCP server."""
    return asyncio.run(_list_tools_async())


def call_mcp_tool(name: str, args: dict) -> str:
    """Execute a tool call over the MCP stdio protocol."""
    return asyncio.run(_call_tool_async(name, args))
