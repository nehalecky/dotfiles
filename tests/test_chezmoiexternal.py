"""Tests for .chezmoiexternal.yaml.tmpl — generalized strata layer composition."""

import subprocess
import tempfile
from pathlib import Path

import yaml

DOTFILES_DIR = Path(__file__).resolve().parent.parent


def _render_external_template(strata_layers: str) -> subprocess.CompletedProcess:
    """Render .chezmoiexternal.yaml.tmpl with a temp config supplying strata_layers data."""
    template_path = DOTFILES_DIR / ".chezmoiexternal.yaml.tmpl"
    config_content = f'[data]\n    strata_layers = "{strata_layers}"\n'
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


def test_external_template_exists():
    """Template file is present."""
    assert (DOTFILES_DIR / ".chezmoiexternal.yaml.tmpl").exists()


def test_external_template_renders_with_no_layers():
    """Template renders valid empty YAML when strata_layers is blank."""
    result = _render_external_template("")
    assert result.returncode == 0, f"Template error: {result.stderr}"
    data = yaml.safe_load(result.stdout)
    assert data is None  # empty YAML


def test_external_template_renders_with_single_layer():
    """Template generates one numbered entry for a single layer URL."""
    result = _render_external_template("git@github.com:nehalecky/strata.rc.git")
    assert result.returncode == 0, f"Template error: {result.stderr}"
    data = yaml.safe_load(result.stdout)
    assert data is not None
    assert ".strata_layer_0/" in data
    assert data[".strata_layer_0/"]["type"] == "git"
    assert data[".strata_layer_0/"]["url"] == "git@github.com:nehalecky/strata.rc.git"


def test_external_template_renders_with_multiple_layers():
    """Template generates numbered entries preserving order for multiple layers."""
    layers = "git@github.com:acme/strata.rc.git,git@github.com:acme/platform.strata.rc.git,git@github.com:nehalecky/strata.rc.git"
    result = _render_external_template(layers)
    assert result.returncode == 0, f"Template error: {result.stderr}"
    data = yaml.safe_load(result.stdout)
    assert data is not None
    assert ".strata_layer_0/" in data
    assert ".strata_layer_1/" in data
    assert ".strata_layer_2/" in data
    assert data[".strata_layer_0/"]["url"] == "git@github.com:acme/strata.rc.git"
    assert data[".strata_layer_1/"]["url"] == "git@github.com:acme/platform.strata.rc.git"
    assert data[".strata_layer_2/"]["url"] == "git@github.com:nehalecky/strata.rc.git"


def test_external_template_trims_whitespace_in_urls():
    """Template trims whitespace around URLs in comma-separated list."""
    layers = " git@github.com:acme/strata.rc.git , git@github.com:nehalecky/strata.rc.git "
    result = _render_external_template(layers)
    assert result.returncode == 0, f"Template error: {result.stderr}"
    data = yaml.safe_load(result.stdout)
    assert data[".strata_layer_0/"]["url"] == "git@github.com:acme/strata.rc.git"
    assert data[".strata_layer_1/"]["url"] == "git@github.com:nehalecky/strata.rc.git"
