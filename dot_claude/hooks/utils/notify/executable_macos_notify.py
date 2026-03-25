#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""macOS notification delivery backend for Claude Code hooks.

Sends a macOS system notification via osascript. Zero external dependencies.
macOS automatically suppresses notifications during Focus/DND mode.

Sounds:
  Glass — soft chime for task completions
  Purr  — attention sound for input-needed events (--urgent)

Usage:
    ./macos_notify.py "Task complete"
    ./macos_notify.py "Input needed" --urgent
    ./macos_notify.py "3 agents done" --subtitle "Session complete"
"""

import argparse
import subprocess
import sys


def notify(message: str, subtitle: str = "", urgent: bool = False) -> bool:
    """Deliver a macOS notification via osascript. Returns True on success."""
    sound = "Purr" if urgent else "Glass"
    # Escape double quotes to prevent AppleScript injection
    safe_msg = message.replace("\\", "\\\\").replace('"', '\\"')
    safe_sub = subtitle.replace("\\", "\\\\").replace('"', '\\"')

    parts = [f'display notification "{safe_msg}"', 'with title "Claude Code"']
    if safe_sub:
        parts.append(f'subtitle "{safe_sub}"')
    parts.append(f'sound name "{sound}"')

    result = subprocess.run(
        ["osascript", "-e", " ".join(parts)],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send macOS notification for Claude Code hooks"
    )
    parser.add_argument("message", nargs="?", default="Task complete")
    parser.add_argument("--subtitle", default="", help="Notification subtitle")
    parser.add_argument(
        "--urgent",
        action="store_true",
        help="Use attention sound (for input-needed events)",
    )
    args = parser.parse_args()

    message = args.message.strip()
    if not message:
        sys.exit(1)

    success = notify(message=message, subtitle=args.subtitle, urgent=args.urgent)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
