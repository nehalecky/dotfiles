"""Tests for compute_enabled_plugins — the B-2 only-true union logic.

Loads the .py.tmpl script directly via importlib (Go template directives live
only in top-of-file comments, so the body is valid Python).
"""

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module loader
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    REPO_ROOT / ".chezmoiscripts" / "run_onchange_after_60-claude-plugins.py.tmpl"
)


def _load_script_module():
    # spec_from_file_location won't auto-detect a .py.tmpl extension as Python,
    # so we supply the SourceFileLoader explicitly.
    from importlib.machinery import SourceFileLoader
    loader = SourceFileLoader("plugins_script", str(SCRIPT_PATH))
    spec = importlib.util.spec_from_loader("plugins_script", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


plugins_script = _load_script_module()
compute_enabled_plugins = plugins_script.compute_enabled_plugins


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_both_sources_empty():
    enabled, sources = compute_enabled_plugins({}, {})
    assert enabled == {}
    assert sources == {}


def test_only_chezmoi_enabled():
    chezmoi = {"plugA@mkt": True, "plugB@mkt": True}
    enabled, sources = compute_enabled_plugins({}, chezmoi)
    assert set(enabled) == {"plugA@mkt", "plugB@mkt"}
    assert all(v is True for v in enabled.values())
    assert sources["plugA@mkt"] == "dot_claude/enabled-plugins.json"
    assert sources["plugB@mkt"] == "dot_claude/enabled-plugins.json"


def test_only_runtime_enabled():
    runtime = {"plugA@mkt": True, "plugB@mkt": True}
    enabled, sources = compute_enabled_plugins(runtime, {})
    assert set(enabled) == {"plugA@mkt", "plugB@mkt"}
    assert sources["plugA@mkt"] == "settings.json"
    assert sources["plugB@mkt"] == "settings.json"


def test_same_key_true_in_both():
    runtime = {"plugA@mkt": True}
    chezmoi = {"plugA@mkt": True}
    enabled, sources = compute_enabled_plugins(runtime, chezmoi)
    assert enabled == {"plugA@mkt": True}
    assert sources["plugA@mkt"] == "both"


def test_different_keys_in_each_source():
    runtime = {"plugA@mkt": True}
    chezmoi = {"plugB@mkt": True}
    enabled, sources = compute_enabled_plugins(runtime, chezmoi)
    assert set(enabled) == {"plugA@mkt", "plugB@mkt"}
    assert sources["plugA@mkt"] == "settings.json"
    assert sources["plugB@mkt"] == "dot_claude/enabled-plugins.json"


@pytest.mark.parametrize("runtime_val,chezmoi_val,expected_source", [
    # True in chezmoi, False in runtime -> present, source = chezmoi
    (False, True, "dot_claude/enabled-plugins.json"),
    # True in runtime, False in chezmoi -> present, source = runtime
    (True, False, "settings.json"),
])
def test_only_true_union_one_side_false(runtime_val, chezmoi_val, expected_source):
    runtime = {"plugX@mkt": runtime_val}
    chezmoi = {"plugX@mkt": chezmoi_val}
    enabled, sources = compute_enabled_plugins(runtime, chezmoi)
    assert "plugX@mkt" in enabled
    assert enabled["plugX@mkt"] is True
    assert sources["plugX@mkt"] == expected_source


def test_false_in_both_excluded():
    runtime = {"plugX@mkt": False}
    chezmoi = {"plugX@mkt": False}
    enabled, sources = compute_enabled_plugins(runtime, chezmoi)
    assert "plugX@mkt" not in enabled
    assert "plugX@mkt" not in sources


def test_runtime_only_missing_from_chezmoi():
    runtime = {"plugA@mkt": True}
    enabled, sources = compute_enabled_plugins(runtime, {})
    assert "plugA@mkt" in enabled
    assert sources["plugA@mkt"] == "settings.json"


def test_mixed_true_false_entries():
    """Keys with at least one True side appear; keys False in both do not."""
    runtime = {"a@m": True, "b@m": False, "c@m": True}
    chezmoi = {"a@m": False, "b@m": False, "d@m": True}
    enabled, sources = compute_enabled_plugins(runtime, chezmoi)
    assert set(enabled) == {"a@m", "c@m", "d@m"}
    assert sources["a@m"] == "settings.json"
    assert sources["c@m"] == "settings.json"
    assert sources["d@m"] == "dot_claude/enabled-plugins.json"
    assert "b@m" not in enabled
