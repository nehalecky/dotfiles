#!/usr/bin/env python3
"""Install Claude Code native binary if not already present."""
import shutil
import subprocess
import sys
from pathlib import Path

INSTALL_URL = "https://claude.ai/install.sh"
CLAUDE_BIN = Path.home() / ".local" / "bin" / "claude"


def main() -> None:
    print("🤖 Checking Claude Code installation...")

    if CLAUDE_BIN.exists() or shutil.which("claude"):
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
        version = result.stdout.strip() if result.returncode == 0 else "unknown"
        print(f"✅ Claude Code already installed ({version})")
        return

    print("Installing Claude Code native binary...")
    fetch = subprocess.run(
        ["curl", "-fsSL", INSTALL_URL],
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        print(f"❌ Failed to download Claude Code installer: {fetch.stderr}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(["/bin/bash"], input=fetch.stdout, text=True)
    if result.returncode != 0:
        print("❌ Claude Code installation failed", file=sys.stderr)
        sys.exit(1)

    if not CLAUDE_BIN.exists():
        print("❌ Claude Code installation may have failed — binary not found at ~/.local/bin/claude", file=sys.stderr)
        sys.exit(1)

    version_result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
    version = version_result.stdout.strip() if version_result.returncode == 0 else "installed"
    print(f"✅ Claude Code installed successfully ({version})")
    print("✨ Binary at ~/.local/bin/claude — auto-updates in the background")


if __name__ == "__main__":
    main()
