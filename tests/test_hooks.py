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
    get_notify_mode,
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

    def test_run_returns_empty_string_on_success_with_no_stdout(self, tmp_script):
        """TTS backends exit 0 with no stdout; run() must return '' not None."""
        b = Backend(name="test", script=tmp_script)
        mock_result = MagicMock(returncode=0, stdout="")
        with patch("utils.common.subprocess.run", return_value=mock_result):
            result = b.run("some text")
        assert result == ""        # success: is not None
        assert result is not None  # caller uses `is not None` to detect success


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

    def test_speak_completion_stops_after_tts_returns_empty_string(self):
        """Empty stdout (real TTS success) must stop the chain — not treated as failure."""
        tts1 = MagicMock()
        tts1.is_available.return_value = True
        tts1.run.return_value = ""  # exit 0, no stdout — real TTS success

        tts2 = MagicMock()
        tts2.is_available.return_value = True

        llm = MagicMock()
        llm.is_available.return_value = True
        llm.run.return_value = "Done!"

        svc = NotificationService(
            tts_backends=[tts1, tts2],
            llm_backends=[llm],
            fallback_messages=FALLBACK_MESSAGES,
        )
        svc.speak_completion()

        tts1.run.assert_called_once()
        tts2.run.assert_not_called()  # chain stopped after tts1 succeeded

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


# ---------------------------------------------------------------------------
# TestGetNotifyMode
# ---------------------------------------------------------------------------


class TestGetNotifyMode:
    def test_default_when_no_file(self, tmp_path, monkeypatch):
        """Returns 'both' when state file does not exist."""
        monkeypatch.setattr("utils.common.MODE_FILE", tmp_path / "nonexistent")
        assert get_notify_mode() == "both"

    def test_reads_valid_mode(self, tmp_path, monkeypatch):
        """Reads mode from state file."""
        f = tmp_path / "notify-mode"
        for mode in ("tts", "macos", "both", "silent"):
            f.write_text(mode + "\n")
            monkeypatch.setattr("utils.common.MODE_FILE", f)
            assert get_notify_mode() == mode

    def test_falls_back_on_unknown_value(self, tmp_path, monkeypatch):
        """Returns 'both' for unrecognised values."""
        f = tmp_path / "notify-mode"
        f.write_text("invalid\n")
        monkeypatch.setattr("utils.common.MODE_FILE", f)
        assert get_notify_mode() == "both"


# ---------------------------------------------------------------------------
# TestBuildServiceModes
# ---------------------------------------------------------------------------


class TestBuildServiceModes:
    def _service_for_mode(self, mode, tmp_path, monkeypatch):
        f = tmp_path / "notify-mode"
        f.write_text(mode + "\n")
        monkeypatch.setattr("utils.common.MODE_FILE", f)
        return build_service()

    def test_tts_mode_no_visual(self, tmp_path, monkeypatch):
        svc = self._service_for_mode("tts", tmp_path, monkeypatch)
        assert len(svc.tts_backends) > 0
        assert len(svc.visual_backends) == 0

    def test_macos_mode_no_tts(self, tmp_path, monkeypatch):
        svc = self._service_for_mode("macos", tmp_path, monkeypatch)
        assert len(svc.tts_backends) == 0
        assert len(svc.visual_backends) > 0

    def test_both_mode_all_backends(self, tmp_path, monkeypatch):
        svc = self._service_for_mode("both", tmp_path, monkeypatch)
        assert len(svc.tts_backends) > 0
        assert len(svc.visual_backends) > 0

    def test_silent_mode_no_backends(self, tmp_path, monkeypatch):
        svc = self._service_for_mode("silent", tmp_path, monkeypatch)
        assert len(svc.tts_backends) == 0
        assert len(svc.visual_backends) == 0

    def test_visual_backends_named_correctly(self, tmp_path, monkeypatch):
        svc = self._service_for_mode("macos", tmp_path, monkeypatch)
        names = [b.name for b in svc.visual_backends]
        assert "macos" in names
        assert "terminal" in names


# ---------------------------------------------------------------------------
# TestDeliverVisual
# ---------------------------------------------------------------------------


class TestDeliverVisual:
    def test_calls_first_available_visual_backend(self):
        available = Backend("mock", Path("/mock"), timeout=5)
        unavailable = Backend("missing", Path("/no/such/file"), timeout=5)
        svc = NotificationService(
            tts_backends=[],
            llm_backends=[],
            fallback_messages=["done"],
            visual_backends=[unavailable, available],
        )
        called_args = []
        available.is_available = lambda: True
        available.run = lambda *a: (called_args.append(a), "")[1] or ""
        svc._deliver_visual("hello")
        # should have called available backend
        assert any("hello" in str(a) for a in called_args)

    def test_urgent_passes_flag(self):
        backend = Backend("mock", Path("/mock"), timeout=5)
        backend.is_available = lambda: True
        received = []
        backend.run = lambda *a: (received.append(a), "")[1] or ""
        svc = NotificationService([], [], ["done"], visual_backends=[backend])
        svc._deliver_visual("alert", urgent=True)
        assert "--urgent" in received[0]


# ---------------------------------------------------------------------------
# TestCompletionMessagePrompt
# Tests the *structure* of the LLM prompt, not LLM output quality (eval
# territory). Deterministic guard against prompt regressions that could
# re-introduce premature or forward-looking completion announcements.
# ---------------------------------------------------------------------------

# Import claude_cli from the hooks source tree
sys.path.insert(0, str(Path(__file__).parent.parent / "dot_claude" / "hooks" / "utils" / "llm"))
import claude_cli  # noqa: E402


class TestCompletionMessagePrompt:
    """Guard against prompt regressions that cause premature announcements."""

    def _capture_prompt(self, context=None):
        """Capture the prompt string built by generate_completion_message."""
        captured = []

        def fake_prompt_llm(prompt_text):
            captured.append(prompt_text)
            return "Task complete."

        with patch.object(claude_cli, "prompt_llm", side_effect=fake_prompt_llm):
            claude_cli.generate_completion_message(context=context)

        return captured[0]

    def test_prompt_constrains_to_completed_actions(self):
        prompt = self._capture_prompt()
        assert "definitively completed" in prompt

    def test_prompt_forbids_future_inference(self):
        prompt = self._capture_prompt()
        assert "Do NOT infer" in prompt or "do NOT infer" in prompt.lower()

    def test_prompt_excludes_specific_outcome_examples(self):
        # "PR merged" was the example that caused premature announcements
        prompt = self._capture_prompt()
        assert "PR merged" not in prompt

    def test_prompt_includes_context_when_provided(self):
        prompt = self._capture_prompt(context="Request: fix bug\nOutcome: tests pass")
        assert "fix bug" in prompt
        assert "tests pass" in prompt

    def test_prompt_omits_context_section_when_none(self):
        prompt = self._capture_prompt(context=None)
        assert "What was just completed" not in prompt
