# 4.2 — MCP Tools vs Resources

## What was broken before
Tools are active actions (running a search, doing math, updating a database). But often models simply need access to static or read-only structured data (like reading course notes or browsing quiz histories). Treating everything as a tool call is cumbersome.

## How it works
MCP explicitly distinguishes:
- **Tools**: Callable functions (`@mcp.tool()`) that take parameters and execute computation.
- **Resources**: URI-addressable readable documents or data feeds (`@mcp.resource("notes://corpus")`) that clients can read like files.
