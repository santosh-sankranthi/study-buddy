"""Switch Study Buddy app state to any target version milestone (v0..v8).

Usage:
    python scripts/switch_version.py v0
    python scripts/switch_version.py v4
    python scripts/switch_version.py v8
"""
import sys
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERSIONS_DIR = REPO_ROOT / "app" / "versions"
MAIN_PY = REPO_ROOT / "app" / "main.py"

def main():
    if len(sys.argv) < 2:
        print("Available versions:")
        for v in sorted(VERSIONS_DIR.iterdir()):
            if v.is_dir():
                print(f"  • {v.name}")
        print("\nUsage: python scripts/switch_version.py <version_tag>")
        sys.exit(1)

    target_ver = sys.argv[1].strip().lower()
    source_py = VERSIONS_DIR / target_ver / "main.py"
    if not source_py.exists():
        print(f"Error: Version '{target_ver}' not found under {VERSIONS_DIR}")
        sys.exit(1)

    shutil.copy(source_py, MAIN_PY)
    print(f"✅ Switched app/main.py to {target_ver.upper()} milestone successfully.")

if __name__ == "__main__":
    main()
