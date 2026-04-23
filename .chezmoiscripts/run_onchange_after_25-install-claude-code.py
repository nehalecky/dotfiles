#!/usr/bin/env python3
"""Install Claude Code native binary, migrating from other install methods if needed."""
import shutil
import subprocess
import sys
from pathlib import Path

# Allow importing from sibling utils/ directory
sys.path.insert(0, str(Path(__file__).parent))
from utils.migration import migration_prompt

INSTALL_URL = "https://claude.ai/install.sh"
CLAUDE_BIN = Path.home() / ".local" / "bin" / "claude"


def install_native() -> None:
    print("🤖 Installing Claude Code native binary...")
    fetch = subprocess.run(["curl", "-fsSL", INSTALL_URL], capture_output=True, text=True)
    if fetch.returncode != 0:
        print(f"❌ Failed to download installer: {fetch.stderr}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(["/bin/bash"], input=fetch.stdout, text=True)
    if result.returncode != 0:
        print("❌ Installation failed", file=sys.stderr)
        sys.exit(1)
    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    print(f"✅ Claude Code native binary installed ({version})")


def detect_source(binary_path: str | None) -> str:
    if not binary_path:
        return "unknown"
    p = Path(binary_path)
    if "homebrew" in str(p).lower() or "npm" in str(p).lower():
        return "npm (Homebrew-managed)"
    if "nvm" in str(p).lower():
        return "npm (nvm-managed)"
    return str(p)


def main() -> None:
    current = shutil.which("claude")
    migration_prompt(
        tool="claude",
        current_binary=current,
        expected_path=CLAUDE_BIN,
        current_source=detect_source(current),
        expected_source="native binary",
        install_fn=install_native,
    )


if __name__ == "__main__":
    main()
