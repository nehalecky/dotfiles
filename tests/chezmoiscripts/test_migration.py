"""Tests for the chezmoi migration utility.

Run from the chezmoi source root:
    python3 -m pytest tests/chezmoiscripts/ -v
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# The migration module lives at ~/.local/lib/chezmoi-scripts/migration.py.
# When running tests in CI or locally before chezmoi apply, fall back to the
# source copy under dot_local/lib/chezmoi-scripts/.
_lib_home = Path.home() / ".local" / "lib" / "chezmoi-scripts"
_lib_source = Path(__file__).parent.parent.parent / "dot_local" / "lib" / "chezmoi-scripts"

for _candidate in (_lib_home, _lib_source):
    if _candidate.exists() and str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))
        break

from migration import ConfigItem, migration_prompt  # noqa: E402

# Path to the scripts directory (for TestDetectSource fixture)
_scripts_dir = Path(__file__).parent.parent.parent / ".chezmoiscripts"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_install_fn() -> MagicMock:
    return MagicMock(name="install_fn")


# ---------------------------------------------------------------------------
# Case 1 — Not installed
# ---------------------------------------------------------------------------

class TestNotInstalled:
    def test_install_fn_called_when_binary_is_none(self, capsys):
        install_fn = _make_install_fn()
        migration_prompt(
            tool="mytool",
            current_binary=None,
            expected_path=Path.home() / ".local/bin/mytool",
            current_source="old source",
            expected_source="new source",
            install_fn=install_fn,
        )
        install_fn.assert_called_once()

    def test_no_migration_prompt_shown(self, capsys):
        install_fn = _make_install_fn()
        migration_prompt(
            tool="mytool",
            current_binary=None,
            expected_path=Path.home() / ".local/bin/mytool",
            current_source="old source",
            expected_source="new source",
            install_fn=install_fn,
        )
        out = capsys.readouterr().out
        # Should NOT show the migration warning header
        assert "Migration available" not in out

    def test_installing_message_printed(self, capsys):
        install_fn = _make_install_fn()
        migration_prompt(
            tool="mytool",
            current_binary=None,
            expected_path=Path.home() / ".local/bin/mytool",
            current_source="old source",
            expected_source="new source",
            install_fn=install_fn,
        )
        out = capsys.readouterr().out
        assert "mytool not found" in out
        assert "new source" in out


# ---------------------------------------------------------------------------
# Case 2 — Already at the expected path
# ---------------------------------------------------------------------------

class TestAlreadyCorrect:
    def test_install_fn_not_called(self, capsys):
        expected = Path.home() / ".local/bin/mytool"
        install_fn = _make_install_fn()

        # Make Path.resolve() return the same path for both sides of comparison
        with patch("migration.Path") as MockPath:
            # Build a fake Path whose .resolve() equals itself for comparison
            fake_path = MagicMock()
            fake_path.resolve.return_value = expected
            MockPath.return_value = fake_path
            MockPath.home.return_value = Path.home()

            migration_prompt(
                tool="mytool",
                current_binary=str(expected),
                expected_path=expected,
                current_source="new source",
                expected_source="new source",
                install_fn=install_fn,
            )
        install_fn.assert_not_called()

    def test_already_correct_via_same_real_path(self, tmp_path, capsys):
        """Integration-style: use real files so resolve() works naturally."""
        binary_file = tmp_path / "mytool"
        binary_file.touch()
        expected = binary_file
        install_fn = _make_install_fn()

        migration_prompt(
            tool="mytool",
            current_binary=str(binary_file),
            expected_path=expected,
            current_source="new source",
            expected_source="new source",
            install_fn=install_fn,
        )
        out = capsys.readouterr().out
        assert "already installed" in out
        install_fn.assert_not_called()

    def test_success_message_printed(self, tmp_path, capsys):
        binary_file = tmp_path / "mytool"
        binary_file.touch()
        install_fn = _make_install_fn()

        migration_prompt(
            tool="mytool",
            current_binary=str(binary_file),
            expected_path=binary_file,
            current_source="new source",
            expected_source="new source",
            install_fn=install_fn,
        )
        out = capsys.readouterr().out
        assert "mytool" in out
        assert "already installed" in out


# ---------------------------------------------------------------------------
# Case 3 — Migration scenarios (current != expected)
# ---------------------------------------------------------------------------

def _migration_prompt_with_different_paths(install_fn, extra_kwargs=None, env=None, isatty=False, user_input="n"):
    """Helper: calls migration_prompt where current != expected to trigger Case 3."""
    extra_kwargs = extra_kwargs or {}
    env = env or {}

    with (
        patch.dict("os.environ", env, clear=False),
        patch("migration.sys") as mock_sys,
        patch("builtins.input", return_value=user_input),
    ):
        mock_sys.stdin.isatty.return_value = isatty
        # Keep real stderr/stdout behaviour for capsys
        mock_sys.stdout = sys.stdout
        mock_sys.stderr = sys.stderr

        migration_prompt(
            tool="mytool",
            current_binary="/usr/local/bin/mytool",   # different from expected
            expected_path=Path.home() / ".local/bin/mytool",
            current_source="old source",
            expected_source="new source",
            install_fn=install_fn,
            **extra_kwargs,
        )


class TestMigrationAutoMigrate:
    """Case 3a — CHEZMOI_AUTO_MIGRATE=1 set."""

    def test_install_fn_called_with_auto_migrate(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            env={"CHEZMOI_AUTO_MIGRATE": "1"},
        )
        install_fn.assert_called_once()

    def test_auto_migrate_message_printed(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            env={"CHEZMOI_AUTO_MIGRATE": "1"},
        )
        out = capsys.readouterr().out
        assert "CHEZMOI_AUTO_MIGRATE=1" in out

    def test_auto_migrate_completion_printed(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            env={"CHEZMOI_AUTO_MIGRATE": "1"},
        )
        out = capsys.readouterr().out
        assert "Migration complete" in out


class TestMigrationInteractiveYes:
    """Case 3b — TTY available, user answers 'y'."""

    def test_install_fn_called_on_yes(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=True,
            user_input="y",
        )
        install_fn.assert_called_once()

    def test_migration_complete_message_on_yes(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=True,
            user_input="y",
        )
        out = capsys.readouterr().out
        assert "Migration complete" in out


class TestMigrationInteractiveNo:
    """Case 3c — TTY available, user answers 'n'."""

    def test_install_fn_not_called_on_no(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=True,
            user_input="n",
        )
        install_fn.assert_not_called()

    def test_keeping_existing_message_on_no(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=True,
            user_input="n",
        )
        out = capsys.readouterr().out
        assert "Keeping existing" in out
        assert "mytool" in out


class TestMigrationNonInteractive:
    """Case 3d — no TTY, no env var."""

    def test_install_fn_not_called(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=False,
        )
        install_fn.assert_not_called()

    def test_guidance_message_printed(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=False,
        )
        out = capsys.readouterr().out
        assert "Non-interactive session detected" in out

    def test_chezmoi_apply_guidance_in_output(self, capsys):
        install_fn = _make_install_fn()
        _migration_prompt_with_different_paths(
            install_fn,
            isatty=False,
        )
        out = capsys.readouterr().out
        assert "chezmoi apply" in out


# ---------------------------------------------------------------------------
# ConfigItem display tests
# ---------------------------------------------------------------------------

class TestConfigItemDisplay:
    """Verify checkmark / dash / warning lines in the config audit section."""

    def _run_with_items(self, config_items, tmp_path, isatty=False):
        """Run migration_prompt in migration state with the given config_items."""
        install_fn = _make_install_fn()
        with (
            patch("migration.sys") as mock_sys,
            patch("builtins.input", return_value="n"),
        ):
            mock_sys.stdin.isatty.return_value = isatty
            mock_sys.stdout = sys.stdout
            mock_sys.stderr = sys.stderr
            migration_prompt(
                tool="mytool",
                current_binary="/usr/local/bin/mytool",
                expected_path=tmp_path / "mytool",
                current_source="old source",
                expected_source="new source",
                install_fn=install_fn,
                config_items=config_items,
            )
        return install_fn

    def test_compatible_existing_shows_checkmark(self, tmp_path, capsys):
        config_file = tmp_path / "config.yml"
        config_file.touch()

        self._run_with_items(
            [ConfigItem(path=config_file, description="user config", compatible=True)],
            tmp_path,
        )
        out = capsys.readouterr().out
        assert "compatible as-is" in out

    def test_absent_config_shows_dash(self, tmp_path, capsys):
        missing = tmp_path / "nonexistent.yml"
        # Do NOT create the file

        self._run_with_items(
            [ConfigItem(path=missing, description="missing config", compatible=True)],
            tmp_path,
        )
        out = capsys.readouterr().out
        assert "not present" in out

    def test_incompatible_config_shows_warning(self, tmp_path, capsys):
        config_file = tmp_path / "config.yml"
        config_file.touch()

        self._run_with_items(
            [ConfigItem(path=config_file, description="bad config", compatible=False)],
            tmp_path,
        )
        out = capsys.readouterr().out
        assert "needs attention" in out

    def test_incompatible_with_migrate_fn_shows_auto_migration_option(self, tmp_path, capsys):
        config_file = tmp_path / "config.yml"
        config_file.touch()
        migrate_fn = MagicMock(name="migrate_fn")

        self._run_with_items(
            [ConfigItem(
                path=config_file,
                description="bad config",
                compatible=False,
                migrate_fn=migrate_fn,
                migrate_description="convert format to v2",
            )],
            tmp_path,
        )
        out = capsys.readouterr().out
        assert "auto-migration available" in out
        assert "convert format to v2" in out

    def test_migrate_fn_called_when_user_confirms(self, tmp_path, capsys):
        config_file = tmp_path / "config.yml"
        config_file.touch()
        migrate_fn = MagicMock(name="migrate_fn")
        install_fn = _make_install_fn()

        with (
            patch("migration.sys") as mock_sys,
            patch("builtins.input", return_value="y"),
        ):
            mock_sys.stdin.isatty.return_value = True
            mock_sys.stdout = sys.stdout
            mock_sys.stderr = sys.stderr
            migration_prompt(
                tool="mytool",
                current_binary="/usr/local/bin/mytool",
                expected_path=tmp_path / "mytool",
                current_source="old source",
                expected_source="new source",
                install_fn=install_fn,
                config_items=[ConfigItem(
                    path=config_file,
                    description="bad config",
                    compatible=False,
                    migrate_fn=migrate_fn,
                    migrate_description="convert format to v2",
                )],
            )
        migrate_fn.assert_called_once()


# ---------------------------------------------------------------------------
# cleanup_hints and post_migration_notes in output
# ---------------------------------------------------------------------------

class TestHintsAndNotes:
    def _run_migration_state(self, tmp_path, extra_kwargs):
        install_fn = _make_install_fn()
        with (
            patch("migration.sys") as mock_sys,
            patch("builtins.input", return_value="n"),
        ):
            mock_sys.stdin.isatty.return_value = False
            mock_sys.stdout = sys.stdout
            mock_sys.stderr = sys.stderr
            migration_prompt(
                tool="mytool",
                current_binary="/usr/local/bin/mytool",
                expected_path=tmp_path / "mytool",
                current_source="old source",
                expected_source="new source",
                install_fn=install_fn,
                **extra_kwargs,
            )

    def test_cleanup_hints_appear_in_output(self, tmp_path, capsys):
        self._run_migration_state(
            tmp_path,
            {"cleanup_hints": ["run `old-pkg remove mytool`"]},
        )
        out = capsys.readouterr().out
        assert "Cleanup after migrating" in out
        assert "old-pkg remove mytool" in out

    def test_post_migration_notes_appear_in_output(self, tmp_path, capsys):
        self._run_migration_state(
            tmp_path,
            {"post_migration_notes": ["check the release notes"]},
        )
        out = capsys.readouterr().out
        assert "After migrating" in out
        assert "check the release notes" in out

    def test_no_cleanup_section_when_hints_absent(self, tmp_path, capsys):
        self._run_migration_state(tmp_path, {})
        out = capsys.readouterr().out
        assert "Cleanup after migrating" not in out

    def test_no_notes_section_when_notes_absent(self, tmp_path, capsys):
        self._run_migration_state(tmp_path, {})
        out = capsys.readouterr().out
        assert "After migrating" not in out


# ---------------------------------------------------------------------------
# detect_source() from the claude install script
# ---------------------------------------------------------------------------

class TestDetectSource:
    """Tests for detect_source() in run_onchange_after_25-install-claude-code.py."""

    @pytest.fixture(autouse=True)
    def _import_detect_source(self):
        # Import from the script module by loading it into sys.modules
        import importlib.util

        script_path = _scripts_dir / "run_onchange_after_25-install-claude-code.py"
        spec = importlib.util.spec_from_file_location(
            "_claude_install_script", script_path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.detect_source = mod.detect_source

    def test_homebrew_path_detected(self):
        result = self.detect_source("/opt/homebrew/bin/claude")
        assert "Homebrew" in result or "npm" in result

    def test_npm_via_homebrew_detected(self):
        result = self.detect_source("/opt/homebrew/lib/node_modules/.bin/claude")
        assert "npm" in result

    def test_nvm_path_detected(self):
        result = self.detect_source("/Users/nico/.nvm/versions/node/v20.0.0/bin/claude")
        assert "nvm" in result

    def test_node_modules_path_detected(self):
        result = self.detect_source("/usr/local/lib/node_modules/@anthropic-ai/claude-code/bin/claude")
        assert "npm" in result

    def test_native_path_returned_as_is(self):
        native = "/Users/nico/.local/bin/claude"
        result = self.detect_source(native)
        # For a native path that matches none of the patterns, the binary path is returned
        assert result == native

    def test_none_binary_returns_unknown(self):
        result = self.detect_source(None)
        assert result == "unknown"
