"""Self-check for Phase 4.1 MCP Servers."""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

class MockServer:
    def __init__(self):
        self.registered = []
    def tool(self):
        def dec(fn):
            self.registered.append(fn.__name__)
            return fn
        return dec

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

    mock = MockServer()
    status = fn(mock)
    assert status is True, "register_grade_tool must return True on success"
    assert "calculate_grade" in mock.registered, "calculate_grade must be registered as a tool"

    print(f"✅ MCP Servers check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
