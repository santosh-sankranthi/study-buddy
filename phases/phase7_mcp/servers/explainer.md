# 7.1 — Model Context Protocol (MCP) Servers

## What was broken before
Previously, all tools were hardwired directly inside Study Buddy's internal Python modules. If another developer or another client application (like Claude Desktop, Cursor, or an IDE) wanted to use our notes search or exam scheduler, they had no standardized way to invoke them.

## How it works
An MCP Server exposes tools, resources, and prompt templates over a standard protocol (stdio or SSE) using JSON-RPC. The official Python MCP SDK (`FastMCP`) makes exposing tools as simple as decorating Python functions with `@mcp.tool()`.
