"""DEMO -- Exposing notes://corpus as an MCP Resource."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from mcp_server.server import get_notes_corpus

corpus = get_notes_corpus()
print("Reading notes://corpus resource (first 150 chars):")
print(corpus[:150], "...")
