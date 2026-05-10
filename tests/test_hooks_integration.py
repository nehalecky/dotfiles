"""Behavioral integration tests for Claude Code hook scripts.

These tests invoke the actual hook executables as subprocesses with JSON
on stdin, verifying real file I/O and exit-code contracts. No TTS fires
during tests — no TTS backends are available in the test environment.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

# Hook scripts live at ~/.claude/hooks/ in HOME (chezmoi-managed)
HOOKS_DIR = Path.home() / ".claude" / "hooks"

# Helpers from common.py (unit tests for the log helpers added in this refactor)
sys.path.insert(0, str(Path(__file__).parent.parent / "dot_claude" / "hooks"))
from utils.common import append_to_log, copy_transcript_to_chat


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run_hook(script: str, input_data: dict, args: tuple = (), env_overrides: dict = None, home=None, cwd=None):
    """Execute a hook script with JSON on stdin. Returns CompletedProcess.

    Pass ``home`` to redirect all ``~/...`` log paths into a temp directory,
    keeping test runs isolated from the real ~/.claude/logs/ directory.
    Pass ``cwd`` to set the working directory of the subprocess (used to
    verify that hooks resolve log paths from __file__, not os.getcwd()).
    """
    env = {**os.environ, **(env_overrides or {})}
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(
        [str(HOOKS_DIR / script), *args],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd) if cwd is not None else None,
        timeout=30,
    )


def make_transcript(tmp_path: Path, lines: list[dict] = None) -> Path:
    """Write a minimal JSONL transcript and return its path."""
    lines = lines or [
        {"type": "user", "message": {"content": "Fix the bug"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Done!"}]}},
    ]
    p = tmp_path / "transcript.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines) + "\n")
    return p


# ---------------------------------------------------------------------------
# TestStopHookBehavior
# ---------------------------------------------------------------------------


class TestStopHookBehavior:
    def test_exits_zero_and_writes_log(self, tmp_path):
        result = run_hook("stop.py", {"event": "stop"}, home=tmp_path)
        assert result.returncode == 0
        log = tmp_path / ".claude" / "logs" / "stop.json"
        assert log.exists()
        data = json.loads(log.read_text())
        assert isinstance(data, list)
        assert data[0] == {"event": "stop"}

    def test_appends_on_multiple_calls(self, tmp_path):
        run_hook("stop.py", {"n": 1}, home=tmp_path)
        run_hook("stop.py", {"n": 2}, home=tmp_path)
        log = tmp_path / ".claude" / "logs" / "stop.json"
        data = json.loads(log.read_text())
        assert len(data) == 2
        assert data[0]["n"] == 1
        assert data[1]["n"] == 2

    def test_chat_flag_writes_chat_json(self, tmp_path):
        transcript = make_transcript(tmp_path)
        result = run_hook(
            "stop.py",
            {"transcript_path": str(transcript)},
            args=("--chat",),
            home=tmp_path,
        )
        assert result.returncode == 0
        chat = tmp_path / ".claude" / "logs" / "chat.json"
        assert chat.exists()
        data = json.loads(chat.read_text())
        assert isinstance(data, list)
        assert len(data) == 2

    def test_chat_flag_missing_transcript_key_no_crash(self, tmp_path):
        result = run_hook("stop.py", {"event": "stop"}, args=("--chat",), home=tmp_path)
        assert result.returncode == 0

    def test_recursion_guard_exits_zero_no_log(self, tmp_path):
        result = run_hook(
            "stop.py",
            {"event": "stop"},
            env_overrides={"_CLAUDE_HOOK_GENERATING": "1"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert not (tmp_path / ".claude" / "logs" / "stop.json").exists()

    def test_invalid_json_exits_zero(self, tmp_path):
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            [str(HOOKS_DIR / "stop.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )
        assert result.returncode == 0


# ---------------------------------------------------------------------------
# TestNotificationHookBehavior
# ---------------------------------------------------------------------------


class TestNotificationHookBehavior:
    def test_exits_zero_and_writes_log(self, tmp_path):
        result = run_hook("notification.py", {"message": "Claude needs input"}, home=tmp_path)
        assert result.returncode == 0
        log = tmp_path / ".claude" / "logs" / "notification.json"
        assert log.exists()
        data = json.loads(log.read_text())
        assert data[0]["message"] == "Claude needs input"

    def test_appends_on_multiple_calls(self, tmp_path):
        run_hook("notification.py", {"message": "first"}, home=tmp_path)
        run_hook("notification.py", {"message": "second"}, home=tmp_path)
        data = json.loads((tmp_path / ".claude" / "logs" / "notification.json").read_text())
        assert len(data) == 2

    def test_recursion_guard_exits_zero_no_log(self, tmp_path):
        result = run_hook(
            "notification.py",
            {"message": "x"},
            env_overrides={"_CLAUDE_HOOK_GENERATING": "1"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert not (tmp_path / ".claude" / "logs" / "notification.json").exists()


# ---------------------------------------------------------------------------
# TestSubagentStopHookBehavior
# ---------------------------------------------------------------------------


class TestSubagentStopHookBehavior:
    def test_exits_zero_and_writes_log(self, tmp_path):
        result = run_hook("subagent_stop.py", {"event": "subagent_stop"}, home=tmp_path)
        assert result.returncode == 0
        log = tmp_path / ".claude" / "logs" / "subagent_stop.json"
        assert log.exists()
        data = json.loads(log.read_text())
        assert data[0] == {"event": "subagent_stop"}

    def test_chat_flag_writes_chat_json(self, tmp_path):
        transcript = make_transcript(tmp_path)
        result = run_hook(
            "subagent_stop.py",
            {"transcript_path": str(transcript)},
            args=("--chat",),
            home=tmp_path,
        )
        assert result.returncode == 0
        assert (tmp_path / ".claude" / "logs" / "chat.json").exists()

    def test_recursion_guard_exits_zero_no_log(self, tmp_path):
        result = run_hook(
            "subagent_stop.py",
            {"event": "subagent_stop"},
            env_overrides={"_CLAUDE_HOOK_GENERATING": "1"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert not (tmp_path / ".claude" / "logs" / "subagent_stop.json").exists()


# ---------------------------------------------------------------------------
# TestAppendToLog (unit tests for the common.py helper)
# ---------------------------------------------------------------------------


class TestAppendToLog:
    def test_creates_file_and_directory(self, tmp_path):
        log_path = str(tmp_path / "sublogs" / "test.json")
        append_to_log(log_path, {"key": "value"})
        data = json.loads(Path(log_path).read_text())
        assert data == [{"key": "value"}]

    def test_appends_to_existing(self, tmp_path):
        log_path = str(tmp_path / "test.json")
        append_to_log(log_path, {"n": 1})
        append_to_log(log_path, {"n": 2})
        data = json.loads(Path(log_path).read_text())
        assert len(data) == 2

    def test_recovers_from_corrupt_file(self, tmp_path):
        log_path = tmp_path / "corrupt.json"
        log_path.write_text("not valid json")
        append_to_log(str(log_path), {"recovered": True})
        data = json.loads(log_path.read_text())
        assert data == [{"recovered": True}]


# ---------------------------------------------------------------------------
# TestCopyTranscriptToChat (unit tests for the common.py helper)
# ---------------------------------------------------------------------------


class TestCopyTranscriptToChat:
    def test_converts_jsonl_to_json_array(self, tmp_path):
        transcript = make_transcript(tmp_path)
        log_dir = str(tmp_path / "logs")
        os.makedirs(log_dir, exist_ok=True)
        copy_transcript_to_chat(str(transcript), log_dir)
        chat = json.loads((Path(log_dir) / "chat.json").read_text())
        assert len(chat) == 2
        assert chat[0]["type"] == "user"

    def test_skips_invalid_jsonl_lines(self, tmp_path):
        transcript = tmp_path / "mixed.jsonl"
        transcript.write_text(
            "bad line\n"
            + json.dumps({"type": "user", "message": {"content": "ok"}})
            + "\n"
        )
        log_dir = str(tmp_path / "logs")
        os.makedirs(log_dir, exist_ok=True)
        copy_transcript_to_chat(str(transcript), log_dir)
        chat = json.loads((Path(log_dir) / "chat.json").read_text())
        assert len(chat) == 1
        assert chat[0]["type"] == "user"

    def test_nonexistent_transcript_does_not_crash(self, tmp_path):
        log_dir = str(tmp_path / "logs")
        os.makedirs(log_dir, exist_ok=True)
        # Should silently swallow the FileNotFoundError
        copy_transcript_to_chat("/nonexistent/path.jsonl", log_dir)
        assert not (Path(log_dir) / "chat.json").exists()


# ---------------------------------------------------------------------------
# TestSessionStartHookBehavior
# Regression test for CWD-leak bug: session_start.py previously used
# Path("logs") (CWD-relative), causing log files to be written into whatever
# directory the parent process had cd'd into (e.g. ~/.zprezto/logs/).
# The fix uses Path(__file__).parent / "logs" so the log always lands next
# to the hook script at ~/.claude/hooks/logs/, regardless of CWD.
# ---------------------------------------------------------------------------


@pytest.fixture
def session_start_log_cleanup():
    """Remove any session_start.json written under HOOKS_DIR/logs/ during the test."""
    log_file = HOOKS_DIR / "logs" / "session_start.json"
    yield log_file
    if log_file.exists():
        log_file.unlink()
    # Remove the logs dir itself only if we created it and it is now empty
    logs_dir = HOOKS_DIR / "logs"
    if logs_dir.exists() and not any(logs_dir.iterdir()):
        logs_dir.rmdir()


def run_session_start(input_data: dict, cwd=None):
    """Invoke session_start.py via python3 (not executable-bit) with JSON on stdin.

    session_start.py is not marked executable in chezmoi (no executable_ prefix),
    so it must be called through the interpreter rather than directly.
    ``cwd`` sets the working directory to simulate a foreign directory like ~/.zprezto/.
    """
    script = HOOKS_DIR / "session_start.py"
    return subprocess.run(
        ["python3", str(script)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd is not None else None,
        timeout=30,
    )


class TestSessionStartHookBehavior:
    def test_log_resolves_to_script_dir_not_cwd(self, tmp_path, session_start_log_cleanup):
        """Regression: log must land in HOOKS_DIR/logs/, not in the CWD.

        Runs session_start.py with CWD set to tmp_path (simulating a foreign
        directory like ~/.zprezto/), then asserts:
          - The log did NOT appear in tmp_path/logs/ (old buggy behaviour).
          - The log DID appear in HOOKS_DIR/logs/ (correct behaviour after fix).
        """
        input_payload = {"hook_event_name": "SessionStart", "session_id": "test-cwd-leak"}
        result = run_session_start(input_payload, cwd=tmp_path)
        assert result.returncode == 0, f"session_start.py exited non-zero: {result.stderr}"

        # Bug would create the log file under the CWD — assert it is absent there.
        cwd_log = tmp_path / "logs" / "session_start.json"
        assert not cwd_log.exists(), (
            f"CWD-leak detected: log written to {cwd_log} instead of HOOKS_DIR/logs/"
        )

        # Fix must write the log next to the script.
        expected_log = session_start_log_cleanup  # HOOKS_DIR / "logs" / "session_start.json"
        assert expected_log.exists(), (
            f"Log not found at expected location {expected_log}; "
            "session_start.py may not have fixed the CWD-relative Path('logs') bug"
        )
