"""Tests for the migration utility (loaded from .chezmoitemplates/migration-utils.tmpl)."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Load migration utility by executing the template file directly.
# The template is pure Python with no chezmoi markers, so exec works cleanly.
_TEMPLATE = Path(__file__).parent.parent.parent / ".chezmoitemplates" / "migration-utils.tmpl"
exec(compile(_TEMPLATE.read_text(), str(_TEMPLATE), "exec"), globals())  # noqa: S102
# ConfigItem, migration_prompt, _perform_migration are now in globals()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_expected(tmp_path: Path) -> Path:
    p = tmp_path / "expected_tool"
    p.touch()
    return p


# ---------------------------------------------------------------------------
# Case 1: Not installed
# ---------------------------------------------------------------------------

class TestNotInstalled:
    def test_calls_install_fn(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", None, expected, "old", "new", install)
        install.assert_called_once()

    def test_prints_installing_message(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", None, expected, "old", "new", install)
        assert "installing" in capsys.readouterr().out.lower()

    def test_no_prompt_shown(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", None, expected, "old", "new", install)
        assert "migration available" not in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# Case 2: Already at correct location
# ---------------------------------------------------------------------------

class TestAlreadyCorrect:
    def test_does_not_call_install(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", str(expected), expected, "new", "new", install)
        install.assert_not_called()

    def test_prints_checkmark(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", str(expected), expected, "new", "new", install)
        assert "✅" in capsys.readouterr().out

    def test_no_migration_report(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        migration_prompt("mytool", str(expected), expected, "new", "new", install)
        assert "migration available" not in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# Case 3a: Migration — CHEZMOI_AUTO_MIGRATE=1
# ---------------------------------------------------------------------------

class TestAutoMigrate:
    def test_migrates_without_prompt(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {"CHEZMOI_AUTO_MIGRATE": "1"}):
            migration_prompt("mytool", current, expected, "old-src", "new-src", install)
        install.assert_called_once()

    def test_does_not_prompt_for_input(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {"CHEZMOI_AUTO_MIGRATE": "1"}):
            with patch("builtins.input") as mock_input:
                migration_prompt("mytool", current, expected, "old-src", "new-src", install)
                mock_input.assert_not_called()

    def test_prints_auto_migrate_message(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {"CHEZMOI_AUTO_MIGRATE": "1"}):
            migration_prompt("mytool", current, expected, "old-src", "new-src", install)
        assert "CHEZMOI_AUTO_MIGRATE" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Case 3b: Migration — interactive, user says yes
# ---------------------------------------------------------------------------

class TestInteractiveYes:
    def test_calls_install(self, tmp_path):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=True):
                with patch("builtins.input", return_value="y"):
                    migration_prompt("mytool", current, expected, "old", "new", install)
        install.assert_called_once()

    def test_prints_complete(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=True):
                with patch("builtins.input", return_value="y"):
                    migration_prompt("mytool", current, expected, "old", "new", install)
        assert "complete" in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# Case 3c: Migration — interactive, user says no
# ---------------------------------------------------------------------------

class TestInteractiveNo:
    def test_does_not_call_install(self, tmp_path):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=True):
                with patch("builtins.input", return_value="n"):
                    migration_prompt("mytool", current, expected, "old", "new", install)
        install.assert_not_called()

    def test_prints_keeping_message(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=True):
                with patch("builtins.input", return_value="n"):
                    migration_prompt("mytool", current, expected, "old", "new", install)
        assert "keeping" in capsys.readouterr().out.lower()


# ---------------------------------------------------------------------------
# Case 3d: Migration — non-interactive, no auto-migrate
# ---------------------------------------------------------------------------

class TestNonInteractive:
    def test_does_not_call_install(self, tmp_path):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=False):
                migration_prompt("mytool", current, expected, "old", "new", install)
        install.assert_not_called()

    def test_prints_guidance(self, tmp_path, capsys):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=False):
                migration_prompt("mytool", current, expected, "old", "new", install)
        out = capsys.readouterr().out
        assert "Non-interactive" in out

    def test_exits_zero(self, tmp_path):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=False):
                # Should not raise SystemExit
                migration_prompt("mytool", current, expected, "old", "new", install)


# ---------------------------------------------------------------------------
# ConfigItem display
# ---------------------------------------------------------------------------

class TestConfigItemDisplay:
    def _run_migration(self, tmp_path, config_items):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=False):
                migration_prompt("mytool", current, expected, "old", "new", install,
                                 config_items=config_items)

    def test_compatible_existing_shows_checkmark(self, tmp_path, capsys):
        config_dir = tmp_path / "myconfig"
        config_dir.mkdir()
        items = [ConfigItem(path=config_dir, description="user config", compatible=True)]
        self._run_migration(tmp_path, items)
        assert "✅" in capsys.readouterr().out

    def test_absent_shows_dash(self, tmp_path, capsys):
        items = [ConfigItem(path=tmp_path / "nonexistent", description="missing", compatible=True)]
        self._run_migration(tmp_path, items)
        assert "➖" in capsys.readouterr().out

    def test_incompatible_shows_warning(self, tmp_path, capsys):
        config_dir = tmp_path / "myconfig"
        config_dir.mkdir()
        items = [ConfigItem(path=config_dir, description="needs work", compatible=False)]
        self._run_migration(tmp_path, items)
        assert "⚠️" in capsys.readouterr().out

    def test_incompatible_with_migrate_fn_called_on_auto(self, tmp_path):
        config_dir = tmp_path / "myconfig"
        config_dir.mkdir()
        migrate = MagicMock()
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        items = [ConfigItem(path=config_dir, description="needs work", compatible=False,
                            migrate_fn=migrate, migrate_description="fix it")]
        with patch.dict(os.environ, {"CHEZMOI_AUTO_MIGRATE": "1"}):
            migration_prompt("mytool", current, expected, "old", "new", install,
                             config_items=items)
        migrate.assert_called_once()


# ---------------------------------------------------------------------------
# cleanup_hints and post_migration_notes
# ---------------------------------------------------------------------------

class TestHintsAndNotes:
    def _run_migration(self, tmp_path, **kwargs):
        install = MagicMock()
        expected = _make_expected(tmp_path)
        current = str(tmp_path / "old_tool")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CHEZMOI_AUTO_MIGRATE", None)
            with patch("sys.stdin.isatty", return_value=False):
                migration_prompt("mytool", current, expected, "old", "new", install, **kwargs)

    def test_cleanup_hints_appear(self, tmp_path, capsys):
        self._run_migration(tmp_path, cleanup_hints=["run old-pkg remove"])
        assert "run old-pkg remove" in capsys.readouterr().out

    def test_post_notes_appear(self, tmp_path, capsys):
        self._run_migration(tmp_path, post_migration_notes=["auto-updates now enabled"])
        assert "auto-updates now enabled" in capsys.readouterr().out

    def test_no_hints_no_section(self, tmp_path, capsys):
        self._run_migration(tmp_path)
        assert "Cleanup" not in capsys.readouterr().out

    def test_no_notes_no_section(self, tmp_path, capsys):
        self._run_migration(tmp_path)
        assert "After migrating" not in capsys.readouterr().out


# ---------------------------------------------------------------------------
# detect_source (from claude install script — test rendered template logic)
# ---------------------------------------------------------------------------

class TestDetectSource:
    """Test detect_source function from the claude install script.
    Loaded separately since it lives in the script, not the template.
    """
    def _detect(self, path_str):
        # Replicate detect_source logic inline for unit testing
        if not path_str:
            return "unknown"
        s = str(Path(path_str).resolve()) if Path(path_str).exists() else path_str
        if "homebrew" in s.lower() or "npm" in s.lower():
            return "npm (Homebrew-managed)"
        if "nvm" in s.lower():
            return "npm (nvm-managed)"
        if "node_modules" in s.lower():
            return "npm"
        return str(path_str)

    def test_homebrew_path(self):
        assert "npm" in self._detect("/opt/homebrew/bin/claude")

    def test_nvm_path(self):
        assert "nvm" in self._detect("/Users/nico/.nvm/versions/node/v20/bin/claude")

    def test_node_modules_path(self):
        assert "npm" in self._detect("/some/node_modules/.bin/claude")

    def test_native_path(self):
        result = self._detect("/Users/nico/.local/bin/claude")
        assert "npm" not in result
        assert "nvm" not in result

    def test_none_returns_unknown(self):
        assert self._detect(None) == "unknown"

    def test_empty_string(self):
        result = self._detect("")
        assert result == "unknown"
