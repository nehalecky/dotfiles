#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Claude CLI LLM backend — uses Claude Code's own auth, zero config required.

Calls `claude -p` non-interactively. No ANTHROPIC_API_KEY needed.

Recursion guard: _CLAUDE_HOOK_GENERATING=1 is set in the subprocess env so
that when `claude -p` finishes and its Stop hook fires, stop.py sees the var
and exits immediately, preventing infinite recursion.
"""

import os
import shutil
import subprocess
import sys
from typing import Optional


def _clean_llm_response(response: Optional[str]) -> Optional[str]:
    """Normalize a raw LLM response to a single clean line, or None."""
    if not response:
        return None
    return response.split("\n")[0].strip().strip('"').strip("'").strip() or None


def prompt_llm(prompt_text):
    """Invoke claude CLI non-interactively and return the response text, or None."""
    if not shutil.which("claude"):
        return None

    try:
        env = {**os.environ, "_CLAUDE_HOOK_GENERATING": "1"}
        result = subprocess.run(
            ["claude", "-p", prompt_text, "--model", "claude-haiku-4-5-20251001"],
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def generate_completion_message(context=None):
    """Generate a short spoken completion announcement. Returns str or None."""
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()
    name_line = (
        f"Optionally (30% of the time) address the engineer by name: {engineer_name}. "
        if engineer_name
        else ""
    )
    context_section = f"What was just completed:\n{context}\n" if context else ""

    prompt = (
        "Generate a short spoken completion announcement for an AI coding assistant.\n"
        "Rules: under 12 words, plain text only, no quotes, return ONLY the announcement.\n"
        f"{name_line}"
        f"{context_section}"
        "Examples: All done! / PR merged and tests passing. / Changes committed successfully.\n"
        "Announcement:"
    )

    return _clean_llm_response(prompt_llm(prompt))


def main():
    if len(sys.argv) < 2:
        print("Usage: claude_cli.py 'prompt' | --completion [--context 'ctx']")
        return

    if sys.argv[1] == "--completion":
        context = None
        if "--context" in sys.argv:
            idx = sys.argv.index("--context")
            if idx + 1 < len(sys.argv):
                context = sys.argv[idx + 1]
        msg = generate_completion_message(context=context)
        if msg:
            print(msg)
        else:
            sys.exit(1)
    else:
        response = prompt_llm(" ".join(sys.argv[1:]))
        print(response or "Error: claude CLI unavailable or no response")


if __name__ == "__main__":
    main()
