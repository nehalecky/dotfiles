#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Install Claude Code native binary, migrating from other distributions if needed.

This script re-runs when its content changes (run_onchange), so migration detection
fires again if the installation method ever changes in the future.
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".local" / "lib" / "chezmoi-scripts"))
from migration import ConfigItem, migration_prompt

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
    print(f"✅ Claude Code installed ({version})")


def detect_source(binary: str | None) -> str:
    if not binary:
        return "unknown"
    s = str(Path(binary).resolve())
    if "homebrew" in s.lower() or "npm" in s.lower():
        return "npm (Homebrew-managed)"
    if "nvm" in s.lower():
        return "npm (nvm-managed)"
    if "node_modules" in s.lower():
        return "npm"
    return str(binary)


def main() -> None:
    current = shutil.which("claude")

    migration_prompt(
        tool="claude",
        current_binary=current,
        expected_path=CLAUDE_BIN,
        current_source=detect_source(current),
        expected_source="native binary",
        install_fn=install_native,
        config_items=[
            ConfigItem(
                path="~/.claude",
                description="settings, plugins, memories, hooks",
                compatible=True,
            ),
        ],
        cleanup_hints=[
            "npm uninstall -g @anthropic-ai/claude-code  # remove the npm package if previously installed",
        ],
        post_migration_notes=[
            "Native binary auto-updates in the background — no more `npm update -g` needed.",
            "Update manually anytime with: claude update",
        ],
    )


if __name__ == "__main__":
    main()
