# Phase 7 Instructor Guide: Model Context Protocol (MCP)

Every tool so far was hand-wired into `app/tools.py` and usable only by *this*
app. MCP replaces that with a standard: a server exposes tools/resources over a
protocol, and any host (Claude Desktop, Cursor, Study Buddy itself) can discover
and call them with no app-specific glue.

## 0. Failure demo — run this before you explain anything (4 min)

```bash
python scripts/switch_version.py v5          # agents work, tools are hand-wired
grep -n "TOOL_REGISTRY" app/tools.py app/agent.py
```

Show that adding a tool means editing `app/tools.py`, then editing anything that
dispatches it. The tool is trapped inside this one app. Landing point: "what if
the tool lived *outside* the app and announced itself over a standard?"

Restore later with `python scripts/switch_version.py v8` (or `v6`).

## Learning objectives

1. Why a standard protocol beats proprietary glue.
2. Build an MCP server exposing tools with the official Python SDK.
3. Distinguish **tools** (compute on demand) from **resources** (readable data).
4. Build an MCP client over stdio JSON-RPC.
5. Where hosts fit, and why the host is a security boundary.

## Timing & pacing (total ~45 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 7.1 Servers | 3 | 6 | 5 | 1 |
| 7.2 Tools vs resources | 2 | 5 | 4 | 1 |
| 7.3 Clients | 2 | 5 | 5 | 2 |
| 7.4 Hosts | 3 | — | — | 5 |

## Live-coding scripts

### 7.1 Servers — `mcp_server/server.py` + `phases/phase7_mcp/servers/`

```bash
python mcp_server/server.py                  # runs the server standalone
python phases/phase7_mcp/servers/demo/main.py
```

Walk `mcp_server/server.py`: each `@mcp_app.tool()` is a plain function with a
docstring; the SDK turns it into a protocol-callable tool. **Twist:** students
wrap their own Phase-6 tool as an MCP server tool instead of the demo's.

### 7.2 Tools vs resources — `phases/phase7_mcp/tools_resources/`

```bash
python phases/phase7_mcp/tools_resources/demo/main.py
```

The server exposes `notes://corpus` as a **resource** (readable data) alongside
the compute tools. Ask the class: "is the notes corpus a tool or a resource?"
**Twist:** students expose a second resource type, e.g. quiz/attempt history
(`quiz://attempts/{session_id}`).

### 7.3 Clients — `phases/phase7_mcp/clients/`

```bash
python phases/phase7_mcp/clients/demo/main.py
```

`app/mcp_client.py` connects to the server over stdio, lists its tools, and can
call one. The app surfaces this at `GET /mcp/tools`. This is **plumbing** —
pre-built, not hand-written live. **Twist (if time):** point the client at a
second, public reference MCP server and list its tools.

### 7.4 Hosts — discussion only

No demo/exercise. Draw the picture: a *host* (Claude Desktop, Cursor, your IDE)
runs *clients* that connect to *servers*. The host decides what to trust —
which is why a malicious server is a real risk.

## Common student mistakes

- **Running the server without a client.** `python mcp_server/server.py` blocks
  on stdio, waiting for JSON-RPC; it is not meant to be opened in a browser.
- **Mixing up tools and resources.** Tools are functions you *call*; resources
  are data you *read* via a URI.
- **Assuming MCP needs the network.** The default transport here is local stdio.
- **Forgetting the repo root on `sys.path`.** The server and client both insert
  the repo root; running them from another directory can break imports.
- **Missing the SDK.** `mcp` is in `requirements.txt` but only imported from
  Phase 7 onward; if it is absent, the client falls back to `app/tools.py`.

## Discussion questions to close

- **What does MCP standardise that an OpenAI tool schema does not?** Discovery
  and transport: a client can enumerate and reach tools without app-specific
  wiring.
- **Why is the host the security boundary?** It chooses which servers to connect
  to and which calls to allow; a compromised server can propose malicious tools.
