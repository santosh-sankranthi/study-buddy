# Phase 7 Instructor Guide: Model Context Protocol (MCP)

## Learning Objectives
1. Understand why standardization beats proprietary tool wiring.
2. Build an MCP Server using the official Python SDK exposing tools and resources.
3. Expose static study notes as readable `notes://corpus` resources.
4. Build an MCP Client using `ClientSession` and `stdio_client`.
5. Discuss host security architectures (Claude Desktop, Cursor, local IDEs).

## Timing & Pacing (Total: 45 min)
- **7.1 MCP Servers (15 min)**: Define tools with `@mcp.tool()`; run server standalone.
- **7.2 Tools vs Resources (10 min)**: Differentiate computation tools from data resources.
- **7.3 MCP Clients (15 min)**: Call tools over stdio JSON-RPC.
- **7.4 MCP Hosts (5 min)**: Architecture discussion on security boundaries.
