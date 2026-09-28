# 7.4 — MCP Hosts (Architectural Discussion)

## What was broken before
Without an architectural understanding of the host layer, developers conflate the client, the host, and the server.

## How it works
- **Host**: The user-facing container that manages authentication, UI, the model context, and tool authorization (e.g. Claude Desktop, Claude Code, Cursor, or our Study Buddy FastAPI app).
- **Client**: The internal adapter inside the host that maintains protocol sessions with servers.
- **Server**: The provider of tools and resources.

## Discussion Questions for the Classroom
1. *Security boundaries:* If any third-party MCP server can expose tools to a host, what stops a malicious server from reading private user files or making unauthorized network requests?
2. *Permissions:* How should a host prompt the user before letting an autonomous agent execute an MCP tool with write access?
