"""Tests for dual-identity git includeIf support (issue #50).

Validates that dot_config/git/config.tmpl:
  - Does NOT emit an includeIf block when profile=personal
  - DOES emit an [includeIf "gitdir:~/work/descript/"] block when profile=work
  - Routes work-repo git config lookups to the work-specific include file

Template rendering tests (fast, no disk I/O beyond chezmoi execute-template):
  test_personal_profile_renders_no_work_block
  test_work_profile_renders_includeif_block

Integration tests (use tmp HOME + chezmoi apply, slower):
  test_work_repo_uses_work_email
  test_outside_pattern_uses_personal_email

Run with: uv tool run pytest tests/test_dual_identity_gitconfig.py -v
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOTFILES_DIR = Path(__file__).resolve().parent.parent
GIT_CONFIG_TMPL = DOTFILES_DIR / "dot_config" / "git" / "config.tmpl"
GIT_CONFIG_WORK_TMPL = DOTFILES_DIR / "dot_config" / "git" / "config-work.tmpl"
TEST_DATA_DIR = DOTFILES_DIR / ".github" / "test-data"

WORK_GIT_EMAIL = "nicholaus.halecky@descript.com"
PERSONAL_GIT_EMAIL = "ci@test.example.com"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _render_template(tmpl_path: Path, profile: str) -> str:
    """Render a chezmoi template with the given profile using test-data config."""
    config_src = TEST_DATA_DIR / f"{profile}.toml"
    assert config_src.exists(), f"test-data not found: {config_src}"

    with open(tmpl_path) as f:
        result = subprocess.run(
            [
                "chezmoi",
                "execute-template",
                f"--source={DOTFILES_DIR}",
                f"--config={config_src}",
            ],
            stdin=f,
            capture_output=True,
            text=True,
        )

    if result.returncode != 0:
        pytest.fail(
            f"chezmoi execute-template failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

    return result.stdout


# ---------------------------------------------------------------------------
# Phase 1 — Template rendering tests (fast, hermetic)
# ---------------------------------------------------------------------------


class TestPersonalProfileRendering:
    def test_personal_profile_renders_no_work_block(self):
        """profile=personal must not emit any includeIf referencing work paths."""
        rendered = _render_template(GIT_CONFIG_TMPL, "personal")
        assert "includeIf" not in rendered, (
            "personal profile must not contain any [includeIf] directives; "
            f"found in rendered output:\n{rendered}"
        )

    def test_personal_profile_renders_no_descript_path(self):
        """profile=personal must not mention the descript work directory."""
        rendered = _render_template(GIT_CONFIG_TMPL, "personal")
        assert "descript" not in rendered.lower(), (
            "personal profile must not reference descript paths; "
            f"found in rendered output:\n{rendered}"
        )


class TestWorkProfileRendering:
    def test_work_profile_renders_includeif_block(self):
        """profile=work must emit [includeIf "gitdir:~/work/descript/"] section."""
        rendered = _render_template(GIT_CONFIG_TMPL, "work")
        assert '[includeIf "gitdir:~/work/descript/"]' in rendered, (
            "work profile must contain [includeIf \"gitdir:~/work/descript/\"] directive; "
            f"rendered output:\n{rendered}"
        )

    def test_work_profile_includeif_has_path_directive(self):
        """The includeIf block in work profile must specify a path = directive."""
        rendered = _render_template(GIT_CONFIG_TMPL, "work")
        # After the includeIf line there must be a path = ... line
        lines = rendered.splitlines()
        found_includeif = False
        found_path = False
        for line in lines:
            stripped = line.strip()
            if '[includeIf "gitdir:~/work/descript/"]' in stripped:
                found_includeif = True
            elif found_includeif and stripped.startswith("path ="):
                found_path = True
                break
            elif found_includeif and stripped.startswith("["):
                # Hit a new section without finding path =
                break
        assert found_includeif, "work profile missing [includeIf] block"
        assert found_path, (
            "work profile [includeIf] block is missing a 'path =' directive; "
            f"rendered output:\n{rendered}"
        )

    def test_work_config_include_file_renders(self):
        """dot_config/git/config-work.tmpl must exist and render without errors."""
        assert GIT_CONFIG_WORK_TMPL.exists(), (
            f"config-work.tmpl does not exist at {GIT_CONFIG_WORK_TMPL} — "
            "create dot_config/git/config-work.tmpl"
        )
        rendered = _render_template(GIT_CONFIG_WORK_TMPL, "work")
        assert rendered.strip(), "config-work.tmpl renders to empty output for profile=work"

    def test_work_config_include_file_has_work_email(self):
        """config-work.tmpl must set user.email to the work email address."""
        assert GIT_CONFIG_WORK_TMPL.exists(), (
            f"config-work.tmpl does not exist at {GIT_CONFIG_WORK_TMPL}"
        )
        rendered = _render_template(GIT_CONFIG_WORK_TMPL, "work")
        assert WORK_GIT_EMAIL in rendered, (
            f"config-work.tmpl must contain work email {WORK_GIT_EMAIL!r}; "
            f"rendered output:\n{rendered}"
        )


# ---------------------------------------------------------------------------
# Phase 2 — Integration tests (use tmp HOME + chezmoi apply)
# ---------------------------------------------------------------------------


@pytest.fixture
def work_home(tmp_path: Path):
    """
    Apply chezmoi with work profile into a temporary HOME directory.

    Returns the tmp_path so tests can create repos and query git config.
    Chezmoi is invoked with --destination=tmp_path using the work test-data config.
    Skips if chezmoi is not available.
    """
    if not _which("chezmoi"):
        pytest.skip("chezmoi not installed")
    if not _which("git"):
        pytest.skip("git not installed")

    config_src = TEST_DATA_DIR / "work.toml"
    if not config_src.exists():
        pytest.skip(f"work test-data not found: {config_src}")

    # Apply chezmoi templates into tmp_path (no scripts, no chezmoiscripts).
    # Use isolated --cache and --persistent-state paths per tmp_path to avoid
    # lock contention with the real chezmoi instance or parallel test runs.
    isolation_dir = tmp_path / ".chezmoi-test"
    isolation_dir.mkdir(parents=True)
    state_file = isolation_dir / "state.boltdb"
    result = subprocess.run(
        [
            "chezmoi",
            "apply",
            "--force",
            "--no-tty",
            f"--source={DOTFILES_DIR}",
            f"--config={config_src}",
            f"--destination={tmp_path}",
            f"--cache={isolation_dir}",
            f"--persistent-state={state_file}",
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(tmp_path)},
    )

    if result.returncode != 0:
        pytest.fail(
            f"chezmoi apply failed for work profile:\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    return tmp_path


def _which(cmd: str) -> bool:
    """Return True if cmd is on PATH."""
    import shutil
    return shutil.which(cmd) is not None


def _git_config(key: str, cwd: Path, home: Path) -> str:
    """Run `git config <key>` in cwd, with HOME overridden to home."""
    result = subprocess.run(
        ["git", "config", key],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "HOME": str(home),
            # Point git to the deployed config in tmp HOME
            "GIT_CONFIG_GLOBAL": str(home / ".config" / "git" / "config"),
        },
    )
    return result.stdout.strip()


class TestIntegration:
    def test_work_repo_uses_work_email(self, work_home: Path):
        """Inside ~/work/descript/, git config user.email must be the work email."""
        # Create a fake repo under the work path
        work_repo = work_home / "work" / "descript" / "test-repo"
        work_repo.mkdir(parents=True)
        subprocess.run(
            ["git", "init"],
            cwd=str(work_repo),
            capture_output=True,
            env={**os.environ, "HOME": str(work_home)},
        )

        email = _git_config("user.email", work_repo, work_home)
        assert email == WORK_GIT_EMAIL, (
            f"Inside ~/work/descript/ expected email {WORK_GIT_EMAIL!r}, got {email!r}"
        )

    def test_outside_pattern_uses_personal_email(self, work_home: Path):
        """Outside ~/work/descript/, git config user.email must be the personal/work global email."""
        # Use a repo outside the work path
        other_repo = work_home / "other-project"
        other_repo.mkdir(parents=True)
        subprocess.run(
            ["git", "init"],
            cwd=str(other_repo),
            capture_output=True,
            env={**os.environ, "HOME": str(work_home)},
        )

        email = _git_config("user.email", other_repo, work_home)
        # The global email from work.toml test-data is ci@work.example.com
        assert email == "ci@work.example.com", (
            f"Outside descript path expected ci@work.example.com, got {email!r}"
        )
