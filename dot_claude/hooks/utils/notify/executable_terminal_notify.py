#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Terminal OSC 9 notification backend for Claude Code hooks.

Writes OSC 9 escape sequence directly to /dev/tty, bypassing stdout piping
in the subprocess context. Supported by WezTerm, kitty, Ghostty, and iTerm2.

WezTerm notification_handling config controls behavior:
  SuppressFromFocusedPane (recommended) — only notifies when terminal is unfocused
  AlwaysShow — always show notification
  NeverShow  — disable

Usage:
    ./terminal_notify.py "Task complete"
"""

import sys


def main() -> None:
    message = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Task complete"
    if not message:
        sys.exit(1)

    try:
        # Write directly to /dev/tty — bypasses captured stdout in hook subprocess
        with open("/dev/tty", "w") as tty:
            # OSC 9: supported by WezTerm, kitty, Ghostty, iTerm2
            tty.write(f"\033]9;{message}\007")
            tty.flush()
    except (OSError, IOError):
        # /dev/tty unavailable (CI, fully piped context) — fail silently
        sys.exit(1)


if __name__ == "__main__":
    main()
