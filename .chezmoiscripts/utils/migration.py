"""Shared migration detection utility for chezmoi run scripts.

When a tool is already installed via a different method (e.g. npm vs. native
binary), ``run_once`` scripts silently skip, leaving the user unaware a
migration is available.  Import ``migration_prompt`` from any chezmoi script to
surface those situations clearly.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable


def migration_prompt(
    tool: str,
    current_binary: str | None,
    expected_path: Path,
    current_source: str,
    expected_source: str,
    install_fn: Callable[[], None],
) -> None:
    """Detect whether a tool needs migrating and act accordingly.

    Args:
        tool: Human-readable tool name (e.g. ``"claude"``).
        current_binary: Absolute path returned by ``shutil.which(tool)``, or
            ``None`` if the tool is not on PATH at all.
        expected_path: The canonical location dotfiles want the binary to live
            (e.g. ``Path.home() / ".local" / "bin" / "claude"``).
        current_source: Human description of the current install method
            (e.g. ``"npm (Homebrew-managed)"``).
        expected_source: Human description of the desired install method
            (e.g. ``"native binary"``).
        install_fn: Zero-argument callable that performs the actual
            installation/migration.  Called when installation or migration is
            accepted.
    """
    # Case 1: tool not installed at all — just install, no prompt needed.
    if current_binary is None:
        install_fn()
        return

    # Case 2: already at the expected location — nothing to do.
    if Path(current_binary).resolve() == expected_path.resolve():
        print(f"✅ {tool} already at expected location ({current_binary})")
        return

    # Case 3: installed via a different method — migration is available.
    print(
        f"⚠️  Migration available: {tool} is currently installed via "
        f"{current_source} ({current_binary}).\n"
        f"   dotfiles now manage {tool} via {expected_source} ({expected_path})."
    )

    auto_migrate = os.environ.get("CHEZMOI_AUTO_MIGRATE") == "1"

    if auto_migrate:
        print(f"   CHEZMOI_AUTO_MIGRATE=1 — migrating automatically.")
        install_fn()
        return

    if sys.stdin.isatty():
        answer = input("   Migrate now? [y/N]: ").strip().lower()
        if answer == "y":
            install_fn()
        else:
            print("   Keeping existing installation.")
        return

    # Non-interactive and auto-migrate not set — inform and continue.
    print(
        "   Run chezmoi apply in an interactive terminal to migrate, "
        "or set CHEZMOI_AUTO_MIGRATE=1 to auto-accept."
    )
