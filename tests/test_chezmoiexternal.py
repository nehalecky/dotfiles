"""Tests for .chezmoiexternal.yaml.tmpl template rendering."""

import subprocess
import tempfile
from pathlib import Path

import yaml

DOTFILES_DIR = Path(__file__).resolve().parent.parent


def _render_external_template(personal_repo_url: str) -> subprocess.CompletedProcess:
    """Render .chezmoiexternal.yaml.tmpl with a temporary config supplying data."""
    template_path = DOTFILES_DIR / ".chezmoiexternal.yaml.tmpl"
    config_content = f'[data]\n    personal_repo_url = "{personal_repo_url}"\n'
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False, prefix="chezmoi-test-"
    ) as cfg:
        cfg.write(config_content)
        cfg_path = cfg.name
    return subprocess.run(
        [
            "chezmoi", "execute-template",
            "--config", cfg_path,
            template_path.read_text(),
        ],
        capture_output=True,
        text=True,
    )


def test_external_template_renders_without_personal_repo():
    """Template renders valid empty YAML when no personal repo configured."""
    template_path = DOTFILES_DIR / ".chezmoiexternal.yaml.tmpl"
    assert template_path.exists(), f"Missing: {template_path}"
    result = _render_external_template("")
    assert result.returncode == 0, f"Template error: {result.stderr}"
    yaml.safe_load(result.stdout)  # must be valid YAML (empty is fine)


def test_external_template_renders_with_personal_repo():
    """Template includes git clone block when personal repo URL provided."""
    result = _render_external_template("git@github.com:nehalecky/strata.rc.git")
    assert result.returncode == 0, f"Template error: {result.stderr}"
    data = yaml.safe_load(result.stdout)
    assert data is not None
    assert ".strata_personal/" in data
