# 2.6 — Model Context Protocol (MCP) Concept

## What was broken before
Right now, every time we want Study Buddy to connect to external data or tools, we write bespoke, hand-crafted Python glue code. If another application (like Claude Desktop or Cursor) wants to access our course notes or tools, we would have to rewrite the integration entirely.

## How it works
Model Context Protocol (MCP) is an open, standardized protocol (like USB-C for AI applications) that lets any host app communicate with any tool or data provider over JSON-RPC. A server exposes tools and resources; any compliant client can discover and use them without knowing how they were implemented.

We will build a real MCP server and client in **Phase 4**. For now, remember: tools and resources can be decoupled from the application and served over a universal protocol.
