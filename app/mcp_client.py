"""Study Buddy MCP Client.

Talks to MCP servers two ways:

* **local**  — the Study Buddy server in ``mcp_server/server.py`` over stdio.
* **external** — a remote MCP server over HTTP (e.g. a live docs server such as
  DeepWiki), so students can watch the app fetch real documentation on the fly.
"""

from __future__ import annotations

import asyncio
import os
import sys
from contextlib import asynccontextmanager
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


# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · External MCP  [Phase 4]
# The same MCP client can point at a REMOTE server over HTTP. The default is a
# live documentation server (DeepWiki), so the class can ask real questions
# about the LangChain docs and watch the answer come back over MCP.
# Override the endpoint/label/tool in .env (MCP_EXTERNAL_*).
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_EXTERNAL_MCP_URL      = "https://mcp.deepwiki.com/mcp"
DEFAULT_EXTERNAL_MCP_LABEL    = "DeepWiki (LangChain docs)"
DEFAULT_EXTERNAL_MCP_ASK_TOOL = "ask_wiki_question"


def external_mcp_config() -> dict:
    """Endpoint and metadata for the external docs MCP server."""
    return {
        "url":      os.getenv("MCP_EXTERNAL_URL", DEFAULT_EXTERNAL_MCP_URL),
        "label":    os.getenv("MCP_EXTERNAL_LABEL", DEFAULT_EXTERNAL_MCP_LABEL),
        "ask_tool": os.getenv("MCP_EXTERNAL_ASK_TOOL", DEFAULT_EXTERNAL_MCP_ASK_TOOL),
    }


@asynccontextmanager
async def _external_session(url: str):
    """Open an initialized MCP session to a remote server (streamable HTTP, else SSE)."""
    if not HAS_MCP:
        raise RuntimeError("The 'mcp' package is not installed")
    from mcp import ClientSession

    try:
        from mcp.client.streamable_http import streamable_http_client as connect
    except ImportError:  # older SDKs use SSE for remote servers
        from mcp.client.sse import sse_client as connect

    async with connect(url) as streams:
        read, write = streams[0], streams[1]
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


async def _list_external_tools_async(url: str) -> list[dict]:
    async with _external_session(url) as session:
        result = await session.list_tools()
        tools = []
        for tool in result.tools:
            schema = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None) or {}
            tools.append({
                "name":         tool.name,
                "description":  tool.description or "",
                "input_schema": schema,
            })
        return tools


async def _call_external_tool_async(url: str, name: str, args: dict) -> str:
    async with _external_session(url) as session:
        result = await session.call_tool(name, args)
        parts = [getattr(block, "text", "") for block in (result.content or [])]
        return "\n".join(part for part in parts if part)


def list_external_tools(url: str | None = None) -> list[dict]:
    """Discover the tools served by the external MCP server (live)."""
    return asyncio.run(_list_external_tools_async(url or external_mcp_config()["url"]))


def call_external_tool(name: str, args: dict | None = None, url: str | None = None) -> str:
    """Call one tool on the external MCP server and return its text result."""
    return asyncio.run(
        _call_external_tool_async(url or external_mcp_config()["url"], name, args or {})
    )
