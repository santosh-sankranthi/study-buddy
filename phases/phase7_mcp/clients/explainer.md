# 7.3 — MCP Clients

## What was broken before
Building an MCP server is half the equation. Our application itself needs to act as an MCP Client when connecting to MCP servers, discovering their tools, and executing calls over the stdio protocol.

## How it works
Using the official Python `mcp` client SDK (`stdio_client` and `ClientSession`), the app connects to the MCP server subprocess, initializes a session, fetches available tool schemas with `session.list_tools()`, and invokes tools with `session.call_tool(name, args)`.
