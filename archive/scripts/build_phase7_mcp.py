from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE7 = REPO_ROOT / "phases" / "phase7_mcp"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── 7.1 MCP Servers ────────────────────────────────────────────────────────────
srv = PHASE7 / "servers"
write(
    srv / "explainer.md",
    """# 7.1 — Model Context Protocol (MCP) Servers

## What was broken before
Previously, all tools were hardwired directly inside Study Buddy's internal Python modules. If another developer or another client application (like Claude Desktop, Cursor, or an IDE) wanted to use our notes search or exam scheduler, they had no standardized way to invoke them.

## How it works
An MCP Server exposes tools, resources, and prompt templates over a standard protocol (stdio or SSE) using JSON-RPC. The official Python MCP SDK (`FastMCP`) makes exposing tools as simple as decorating Python functions with `@mcp.tool()`.
"""
)

write(
    srv / "demo/main.py",
    """\"\"\"DEMO -- Exposing Tools via FastMCP Server.

The instructor demonstrates defining and inspecting an MCP server.
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from mcp_server.server import mcp_app

print("MCP Server initialized:", getattr(mcp_app, "name", "StudyBuddy"))
if hasattr(mcp_app, "_tool_manager"):
    tools = list(mcp_app._tool_manager._tools.keys())
    print("Registered MCP Tools:", tools)
else:
    print("MCP Server ready to accept client connections over stdio.")
"""
)

write(
    srv / "exercise/main.py",
    """\"\"\"EXERCISE -- Add calculate_grade to MCP Server.

The demo exposed search_notes and get_exam_schedule as MCP tools.
Your twist: register calculate_grade in the MCP server so clients can
calculate weighted averages over the standard protocol.

Run when done:
    python phases/phase7_mcp/servers/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): In mcp_server/server.py (or implement below):
#   Import calculate_grade from app.tools
#   Expose it with @mcp_app.tool()

def register_grade_tool(server) -> bool:
    \"\"\"Register calculate_grade with server and return True if successful.\"\"\"
    raise NotImplementedError("TODO(1): register calculate_grade on the MCP server")


if __name__ == "__main__":
    from mcp_server.server import mcp_app
    print("Registration status:", register_grade_tool(mcp_app))
"""
)

write(
    srv / "solution/main.py",
    """\"\"\"SOLUTION -- Add calculate_grade to MCP Server.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade
from mcp_server.server import mcp_app

def register_grade_tool(server) -> bool:
    if hasattr(server, "tool"):
        server.tool()(calculate_grade)
        return True
    return False

if __name__ == "__main__":
    print("Registration status:", register_grade_tool(mcp_app))
"""
)

write(
    srv / "solution/check.py",
    """\"\"\"Self-check for Phase 7.1 MCP Servers.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("srv_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "register_grade_tool", None)
    assert fn is not None, "register_grade_tool function must be defined"

    # Also verify mcp_server/server.py contains calculate_grade
    server_code = (HERE.parents[3] / "mcp_server" / "server.py").read_text()
    assert "calculate_grade" in server_code, "calculate_grade must be in mcp_server/server.py"

    print(f"✅ MCP Servers check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── 7.2 MCP Tools & Resources ──────────────────────────────────────────────────
res = PHASE7 / "tools_resources"
write(
    res / "explainer.md",
    """# 7.2 — MCP Tools vs Resources

## What was broken before
Tools are active actions (running a search, doing math, updating a database). But often models simply need access to static or read-only structured data (like reading course notes or browsing quiz histories). Treating everything as a tool call is cumbersome.

## How it works
MCP explicitly distinguishes:
- **Tools**: Callable functions (`@mcp.tool()`) that take parameters and execute computation.
- **Resources**: URI-addressable readable documents or data feeds (`@mcp.resource("notes://corpus")`) that clients can read like files.
"""
)

write(
    res / "demo/main.py",
    """\"\"\"DEMO -- Exposing notes://corpus as an MCP Resource.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from mcp_server.server import get_notes_corpus

corpus = get_notes_corpus()
print("Reading notes://corpus resource (first 150 chars):")
print(corpus[:150], "...")
"""
)

write(
    res / "exercise/main.py",
    """\"\"\"EXERCISE -- Expose Quiz History as an MCP Resource.

The demo exposed notes://corpus.
Your twist: expose a session quiz history resource at 'quiz://attempts/{session_id}'.

Run when done:
    python phases/phase7_mcp/tools_resources/solution/check.py
\"\"\"
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement get_quiz_attempts(session_id: str) -> str
#   Return a JSON-encoded dict with {"session_id": session_id, "attempts": []}

def get_quiz_attempts(session_id: str) -> str:
    raise NotImplementedError("TODO(1): implement get_quiz_attempts")


if __name__ == "__main__":
    res = get_quiz_attempts("session_42")
    print("Quiz resource output:", res)
"""
)

write(
    res / "solution/main.py",
    """\"\"\"SOLUTION -- Expose Quiz History as an MCP Resource.\"\"\"
import json

def get_quiz_attempts(session_id: str) -> str:
    return json.dumps({"session_id": session_id, "attempts": []})

if __name__ == "__main__":
    print(get_quiz_attempts("session_42"))
"""
)

write(
    res / "solution/check.py",
    """\"\"\"Self-check for Phase 7.2 MCP Tools & Resources.\"\"\"
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("res_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "get_quiz_attempts", None)
    assert fn is not None, "get_quiz_attempts must be defined"

    raw = fn("session_123")
    data = json.loads(raw)
    assert data.get("session_id") == "session_123", "Must include session_id in JSON"
    assert "attempts" in data, "Must include attempts in JSON"

    print(f"✅ MCP Resources check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── 7.3 MCP Clients ────────────────────────────────────────────────────────────
cli = PHASE7 / "clients"
write(
    cli / "explainer.md",
    """# 7.3 — MCP Clients

## What was broken before
Building an MCP server is half the equation. Our application itself needs to act as an MCP Client when connecting to MCP servers, discovering their tools, and executing calls over the stdio protocol.

## How it works
Using the official Python `mcp` client SDK (`stdio_client` and `ClientSession`), the app connects to the MCP server subprocess, initializes a session, fetches available tool schemas with `session.list_tools()`, and invokes tools with `session.call_tool(name, args)`.
"""
)

write(
    cli / "demo/main.py",
    """\"\"\"DEMO -- Listing Tools via MCP Client.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import list_mcp_tools

tools = list_mcp_tools()
print(f"Connected to MCP Server. Found {len(tools)} tools:")
for t in tools:
    name = t.get("name") if isinstance(t, dict) else getattr(t, "name", str(t))
    print("  •", name)
"""
)

write(
    cli / "exercise/main.py",
    """\"\"\"EXERCISE -- Call calculate_grade through MCP Client.

The demo listed MCP tools.
Your twist: execute calculate_grade through the MCP protocol end-to-end.

Run when done:
    python phases/phase7_mcp/clients/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import call_mcp_tool

# TODO(1): Call call_mcp_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]})
#   Store the result in `grade_result` and print it.

grade_result = ""


if __name__ == "__main__":
    # TODO(2): Uncomment and run once implemented:
    # assert grade_result != "", "TODO: assign grade_result"
    print("MCP grade result:", grade_result)
"""
)

write(
    cli / "solution/main.py",
    """\"\"\"SOLUTION -- Call calculate_grade through MCP Client.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.mcp_client import call_mcp_tool

grade_result = call_mcp_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]})

if __name__ == "__main__":
    print("MCP grade result:", grade_result)
"""
)

write(
    cli / "solution/check.py",
    """\"\"\"Self-check for Phase 7.3 MCP Clients.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("cli_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    res = getattr(mod, "grade_result", "")
    assert isinstance(res, str) and len(res.strip()) > 0, "grade_result must be a non-empty string"
    assert "91" in res or "92" in res or "%" in res, f"Expected grade percentage, got: {res}"

    print(f"✅ MCP Clients check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── 7.4 MCP Hosts ──────────────────────────────────────────────────────────────
write(
    PHASE7 / "hosts/explainer.md",
    """# 7.4 — MCP Hosts (Architectural Discussion)

## What was broken before
Without an architectural understanding of the host layer, developers conflate the client, the host, and the server.

## How it works
- **Host**: The user-facing container that manages authentication, UI, the model context, and tool authorization (e.g. Claude Desktop, Claude Code, Cursor, or our Study Buddy FastAPI app).
- **Client**: The internal adapter inside the host that maintains protocol sessions with servers.
- **Server**: The provider of tools and resources.

## Discussion Questions for the Classroom
1. *Security boundaries:* If any third-party MCP server can expose tools to a host, what stops a malicious server from reading private user files or making unauthorized network requests?
2. *Permissions:* How should a host prompt the user before letting an autonomous agent execute an MCP tool with write access?
"""
)

print("Created Phase 7 MCP concepts successfully.")
