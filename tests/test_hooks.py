"""Comprehensive pytest tests for the Claude Code hook notification system."""

import json
import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Allow importing from the hooks source tree (chezmoi layout)
sys.path.insert(0, str(Path(__file__).parent.parent / "dot_claude" / "hooks"))

from utils.common import (
    FALLBACK_MESSAGES,
    Backend,
    NotificationService,
    TranscriptParser,
    build_service,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_script(tmp_path):
    """Create a temporary script file that exists on disk."""
    script = tmp_path / "fake_script.py"
    script.write_text("# placeholder")
    return script


@pytest.fixture
def missing_script(tmp_path):
    """Return a Path that does not exist."""
    return tmp_path / "does_not_exist.py"


@pytest.fixture
def transcript_file(tmp_path):
    """Create a sample JSONL transcript file."""
    lines = [
        json.dumps({
            "type": "user",
            "message": {"content": "Please fix the login bug"},
        }),
        json.dumps({
            "type": "assistant",
            "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "pytest tests/"}},
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "/home/user/src/auth.py"}},
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "/home/user/src/auth.py"}},
                {"type": "tool_use", "name": "Grep", "input": {"pattern": "login"}},
                {"type": "text", "text": "Fixed the authentication issue."},
            ]},
        }),
    ]
    f = tmp_path / "transcript.jsonl"
    f.write_text("\n".join(lines) + "\n")
    return f


def _make_backend(tmp_path, name="test", env_key=None, timeout=15, exists=True):
    """Helper to create a Backend with a real or missing script path."""
    script = tmp_path / f"{name}.py"
    if exists:
        script.write_text("# placeholder")
    return Backend(name=name, script=script, env_key=env_key, timeout=timeout)


# ---------------------------------------------------------------------------
# TestBackend
# ---------------------------------------------------------------------------


class TestBackend:
    def test_is_available_true_no_env_key(self, tmp_script):
        b = Backend(name="test", script=tmp_script)
        assert b.is_available() is True

    def test_is_available_false_script_missing(self, missing_script):
        b = Backend(name="test", script=missing_script)
        assert b.is_available() is False

    def test_is_available_false_env_key_not_set(self, tmp_script, monkeypatch):
        monkeypatch.delenv("SOME_SECRET_KEY", raising=False)
        b = Backend(name="test", script=tmp_script, env_key="SOME_SECRET_KEY")
        assert b.is_available() is False

    def test_is_available_true_env_key_set(self, tmp_script, monkeypatch):
        monkeypatch.setenv("SOME_SECRET_KEY", "abc123")
        b = Backend(name="test", script=tmp_script, env_key="SOME_SECRET_KEY")
        assert b.is_available() is True

    def test_run_returns_stripped_stdout(self, tmp_script):
        b = Backend(name="test", script=tmp_script)
        mock_result = MagicMock(returncode=0, stdout="  hello world  \n")
        with patch("utils.common.subprocess.run", return_value=mock_result) as mock_run:
            result = b.run("arg1", "arg2")
        assert result == "hello world"
        mock_run.assert_called_once_with(
            ["uv", "run", str(tmp_script), "arg1", "arg2"],
            capture_output=True,
            text=True,
            timeout=15,
        )

    def test_run_returns_none_on_nonzero_returncode(self, tmp_script):
        b = Backend(name="test", script=tmp_script)
        mock_result = MagicMock(returncode=1, stdout="error output")
        with patch("utils.common.subprocess.run", return_value=mock_result):
            assert b.run() is None

    def test_run_returns_none_on_timeout(self, tmp_script):
        b = Backend(name="test", script=tmp_script)
        with patch("utils.common.subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 15)):
            assert b.run() is None

    def test_run_returns_none_on_file_not_found(self, tmp_script):
        b = Backend(name="test", script=tmp_script)
        with patch("utils.common.subprocess.run", side_effect=FileNotFoundError):
            assert b.run() is None


# ---------------------------------------------------------------------------
# TestTranscriptParser
# ---------------------------------------------------------------------------


class TestTranscriptParser:
    def test_returns_none_for_missing_file(self):
        assert TranscriptParser.parse("/nonexistent/file.jsonl") is None

    def test_returns_none_for_none_path(self):
        assert TranscriptParser.parse(None) is None

    def test_returns_none_for_empty_transcript(self, tmp_path):
        f = tmp_path / "empty.jsonl"
        f.write_text("")
        assert TranscriptParser.parse(str(f)) is None

    def test_extracts_last_user_message(self, transcript_file):
        result = TranscriptParser.parse(str(transcript_file))
        assert result is not None
        assert "Request: Please fix the login bug" in result

    def test_extracts_bash_tool_actions(self, transcript_file):
        result = TranscriptParser.parse(str(transcript_file))
        assert result is not None
        assert "Bash(pytest tests/)" in result

    def test_deduplicates_edit_tool_calls(self, transcript_file):
        result = TranscriptParser.parse(str(transcript_file))
        assert result is not None
        # Edit on auth.py appears twice in input but should appear once in output
        actions_line = [l for l in result.split("\n") if l.startswith("Actions:")][0]
        assert actions_line.count("Edit src/auth.py") == 1

    def test_extracts_last_assistant_text_as_outcome(self, transcript_file):
        result = TranscriptParser.parse(str(transcript_file))
        assert result is not None
        assert "Outcome: Fixed the authentication issue." in result

    def test_handles_malformed_jsonl_gracefully(self, tmp_path):
        f = tmp_path / "bad.jsonl"
        f.write_text(
            "not valid json\n"
            + json.dumps({"type": "user", "message": {"content": "hello"}})
            + "\n"
        )
        result = TranscriptParser.parse(str(f))
        assert result is not None
        assert "Request: hello" in result

    def test_limits_tool_actions_to_last_8(self, tmp_path):
        blocks = []
        for i in range(15):
            blocks.append({
                "type": "tool_use",
                "name": "Bash",
                "input": {"command": f"command_{i}"},
            })
        entry = {
            "type": "assistant",
            "message": {"content": blocks},
        }
        f = tmp_path / "many_tools.jsonl"
        f.write_text(json.dumps(entry) + "\n")
        result = TranscriptParser.parse(str(f))
        assert result is not None
        actions_line = [l for l in result.split("\n") if l.startswith("Actions:")][0]
        # Should contain exactly 8 Bash entries (the last 8)
        assert actions_line.count("Bash(") == 8


# ---------------------------------------------------------------------------
# TestNotificationService
# ---------------------------------------------------------------------------


class TestNotificationService:
    def test_speak_completion_calls_tts_with_llm_message(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")
        llm = _make_backend(tmp_path, name="llm1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[llm],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(llm, "is_available", return_value=True), \
             patch.object(llm, "run", return_value="All tests pass!") as llm_run, \
             patch.object(tts, "run") as tts_run:
            svc.speak_completion()

        llm_run.assert_called_once()
        tts_run.assert_called_once_with("All tests pass!")

    def test_speak_completion_skips_when_no_tts(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1", exists=False)
        llm = _make_backend(tmp_path, name="llm1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[llm],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(llm, "run") as llm_run:
            svc.speak_completion()

        llm_run.assert_not_called()

    def test_speak_completion_uses_fallback_when_all_llm_fail(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")
        llm = _make_backend(tmp_path, name="llm1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[llm],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(llm, "is_available", return_value=True), \
             patch.object(llm, "run", return_value=None), \
             patch.object(tts, "run") as tts_run:
            svc.speak_completion()

        tts_run.assert_called_once()
        spoken = tts_run.call_args[0][0]
        assert spoken in FALLBACK_MESSAGES

    def test_speak_completion_falls_through_to_second_tts_when_first_run_fails(self):
        """First TTS is available but run() returns None; second TTS should be used."""
        tts1 = MagicMock()
        tts1.is_available.return_value = True
        tts1.run.return_value = None  # simulates timeout / audio failure

        tts2 = MagicMock()
        tts2.is_available.return_value = True
        tts2.run.return_value = "spoken"

        llm = MagicMock()
        llm.is_available.return_value = True
        llm.run.return_value = "Done!"

        svc = NotificationService(
            tts_backends=[tts1, tts2],
            llm_backends=[llm],
            fallback_messages=FALLBACK_MESSAGES,
        )
        svc.speak_completion()

        tts1.run.assert_called_once_with("Done!")
        tts2.run.assert_called_once_with("Done!")

    def test_speak_notification_falls_through_to_second_tts_when_first_run_fails(self):
        """First TTS is available but run() returns None; second TTS should be used."""
        tts1 = MagicMock()
        tts1.is_available.return_value = True
        tts1.run.return_value = None

        tts2 = MagicMock()
        tts2.is_available.return_value = True
        tts2.run.return_value = "spoken"

        svc = NotificationService(
            tts_backends=[tts1, tts2],
            llm_backends=[],
            fallback_messages=FALLBACK_MESSAGES,
        )
        svc.speak_notification("hello")

        tts1.run.assert_called_once_with("hello")
        tts2.run.assert_called_once_with("hello")

    def test_speak_completion_skips_unavailable_llm(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")
        llm1 = _make_backend(tmp_path, name="llm_bad")
        llm2 = _make_backend(tmp_path, name="llm_good")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[llm1, llm2],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(llm1, "is_available", return_value=False), \
             patch.object(llm2, "is_available", return_value=True), \
             patch.object(llm1, "run") as llm1_run, \
             patch.object(llm2, "run", return_value="Done!") as llm2_run, \
             patch.object(tts, "run") as tts_run:
            svc.speak_completion()

        llm1_run.assert_not_called()
        llm2_run.assert_called_once()
        tts_run.assert_called_once_with("Done!")

    def test_speak_notification_verbatim_for_real_content(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(tts, "run") as tts_run:
            svc.speak_notification("Please review the PR")

        tts_run.assert_called_once_with("Please review the PR")

    def test_speak_notification_generic_for_placeholder(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(tts, "run") as tts_run:
            svc.speak_notification("Claude is waiting for your input")

        tts_run.assert_called_once()
        spoken = tts_run.call_args[0][0]
        assert "input is needed" in spoken

    def test_speak_notification_truncates_to_200_chars(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[],
            fallback_messages=FALLBACK_MESSAGES,
        )

        long_message = "x" * 300

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(tts, "run") as tts_run:
            svc.speak_notification(long_message)

        tts_run.assert_called_once()
        spoken = tts_run.call_args[0][0]
        assert len(spoken) == 200

    def test_llm_priority_first_available_wins(self, tmp_path):
        tts = _make_backend(tmp_path, name="tts1")
        llm1 = _make_backend(tmp_path, name="llm1")
        llm2 = _make_backend(tmp_path, name="llm2")

        svc = NotificationService(
            tts_backends=[tts],
            llm_backends=[llm1, llm2],
            fallback_messages=FALLBACK_MESSAGES,
        )

        with patch.object(tts, "is_available", return_value=True), \
             patch.object(llm1, "is_available", return_value=True), \
             patch.object(llm2, "is_available", return_value=True), \
             patch.object(llm1, "run", return_value="First wins!") as llm1_run, \
             patch.object(llm2, "run") as llm2_run, \
             patch.object(tts, "run"):
            svc.speak_completion()

        llm1_run.assert_called_once()
        llm2_run.assert_not_called()


# ---------------------------------------------------------------------------
# TestBuildService
# ---------------------------------------------------------------------------


class TestBuildService:
    def test_returns_notification_service(self, tmp_path):
        svc = build_service(hooks_dir=tmp_path)
        assert isinstance(svc, NotificationService)

    def test_tts_backends_in_correct_order(self, tmp_path):
        svc = build_service(hooks_dir=tmp_path)
        names = [b.name for b in svc.tts_backends]
        assert names == ["elevenlabs", "openai", "kokoro", "pyttsx3"]

    def test_llm_backends_in_correct_order(self, tmp_path):
        svc = build_service(hooks_dir=tmp_path)
        names = [b.name for b in svc.llm_backends]
        assert names == ["claude_cli", "openai", "anthropic", "ollama"]


# Recursion guard behavior is tested behaviorally in test_hooks_integration.py:
# TestStopHookBehavior::test_recursion_guard_exits_zero_no_log
# TestNotificationHookBehavior::test_recursion_guard_exits_zero_no_log
# TestSubagentStopHookBehavior::test_recursion_guard_exits_zero_no_log
