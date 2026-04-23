"""Shared migration utility for chezmoi scripts.

Usage pattern for any script that manages a tool installation:

    from utils.migration import ConfigItem, migration_prompt

    migration_prompt(
        tool="mytool",
        current_binary=shutil.which("mytool"),
        expected_path=Path.home() / ".local/bin/mytool",
        current_source="old distribution method",
        expected_source="new distribution method",
        install_fn=do_install,
        config_items=[
            ConfigItem(
                path=Path.home() / ".config/mytool",
                description="user config",
                compatible=True,  # True = confirm compatible, False = needs attention
                migrate_fn=None,  # None = inform only, callable = auto-migrate
            ),
        ],
        cleanup_hints=["run `old-pkg remove mytool` to clean up the old install"],
        post_migration_notes=["new distribution auto-updates; no manual update needed"],
    )
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class ConfigItem:
    path: Path | str
    description: str
    compatible: bool = True        # True = compatible as-is, False = needs attention
    migrate_fn: Callable | None = None  # If provided, offered as auto-migration
    migrate_description: str = ""  # Human description of what migrate_fn does


def migration_prompt(
    tool: str,
    current_binary: str | None,
    expected_path: Path,
    current_source: str,
    expected_source: str,
    install_fn: Callable,
    config_items: list[ConfigItem] | None = None,
    cleanup_hints: list[str] | None = None,
    post_migration_notes: list[str] | None = None,
) -> None:
    """Detect installation state and guide migration if needed."""
    config_items = config_items or []
    cleanup_hints = cleanup_hints or []
    post_migration_notes = post_migration_notes or []

    # Case 1: Not installed at all — install directly, no migration needed
    if current_binary is None:
        print(f"🤖 {tool} not found — installing via {expected_source}...")
        install_fn()
        return

    # Case 2: Already at expected location — nothing to do
    try:
        already_correct = Path(current_binary).resolve() == Path(expected_path).resolve()
    except (OSError, ValueError):
        already_correct = False

    if already_correct:
        print(f"✅ {tool} already installed via {expected_source} ({expected_path})")
        return

    # Case 3: Installed via a different method — migration available
    print(f"\n⚠️  Migration available: {tool}")
    print(f"   Currently: {current_source} → {current_binary}")
    print(f"   dotfiles now use: {expected_source} → {expected_path}")

    # Config audit
    if config_items:
        print("\n   Configuration review:")
        for item in config_items:
            p = Path(item.path).expanduser()
            exists = p.exists()
            if not exists:
                print(f"   ➖ {item.path} — not present, nothing to migrate")
            elif item.compatible:
                print(f"   ✅ {item.path} — {item.description}, compatible as-is")
            else:
                print(f"   ⚠️  {item.path} — {item.description}, needs attention")
                if item.migrate_fn and item.migrate_description:
                    print(f"         → auto-migration available: {item.migrate_description}")

    # Cleanup hints
    if cleanup_hints:
        print("\n   Cleanup after migrating:")
        for hint in cleanup_hints:
            print(f"   ℹ️  {hint}")

    # Post-migration notes
    if post_migration_notes:
        print("\n   After migrating:")
        for note in post_migration_notes:
            print(f"   • {note}")

    print()

    # Determine if we should auto-migrate
    auto = os.environ.get("CHEZMOI_AUTO_MIGRATE") == "1"
    interactive = sys.stdin.isatty()

    if auto:
        print(f"   CHEZMOI_AUTO_MIGRATE=1 — proceeding with migration...")
        _perform_migration(tool, config_items, install_fn)
        return

    if not interactive:
        print(
            f"   Non-interactive session detected. To migrate:\n"
            f"   • Run `chezmoi apply` in an interactive terminal, or\n"
            f"   • Set CHEZMOI_AUTO_MIGRATE=1 and run `chezmoi apply`\n"
            f"   Keeping existing {tool} installation for now."
        )
        return

    answer = input(f"   Migrate now? [y/N]: ").strip().lower()
    if answer == "y":
        _perform_migration(tool, config_items, install_fn)
    else:
        print(f"   Keeping existing {tool} installation.")


def _perform_migration(tool: str, config_items: list[ConfigItem], install_fn: Callable) -> None:
    # Run any config auto-migrations first
    for item in config_items:
        if item.migrate_fn and not item.compatible:
            p = Path(item.path).expanduser()
            if p.exists():
                print(f"   🔄 Migrating {item.path}...")
                item.migrate_fn()

    # Install the new binary
    install_fn()
    print(f"✅ Migration complete.")
