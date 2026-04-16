#!/usr/bin/env python3
"""
CI test script for chezmoi dotfiles repository.
Tests template rendering, syntax validation, script linting, and hook validation.
Usage: PROFILE=personal TERMINAL=wezterm python3 tests/ci-test.py
"""
import contextlib
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROFILE = os.environ.get("PROFILE", "personal")
TERMINAL = os.environ.get("TERMINAL", "wezterm")
DOTFILES_DIR = Path(
    os.environ.get("DOTFILES_DIR", Path(__file__).resolve().parent.parent)
)

PASS_COUNT = 0
FAIL_COUNT = 0

USE_COLOR = sys.stdout.isatty()
GREEN = "\033[0;32m" if USE_COLOR else ""
RED = "\033[0;31m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def pass_test(label: str) -> None:
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"{GREEN}[PASS]{RESET} {label}")


def fail_test(label: str, detail: str = "") -> None:
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"{RED}[FAIL]{RESET} {label}")
    if detail:
        print(detail, file=sys.stderr)


def run(*cmd: str, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ---------------------------------------------------------------------------
# TOML validation helper
# ---------------------------------------------------------------------------


def validate_toml(path: str) -> bool:
    """Validate a TOML file using Python's tomllib (3.11+) or tomli fallback."""
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            print("ERROR: no tomllib/tomli available", file=sys.stderr)
            sys.exit(1)
    with open(path, "rb") as f:
        tomllib.load(f)
    return True


# ---------------------------------------------------------------------------
# Config context manager — fixes H1, H2, M3 from bash version
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def chezmoi_config(
    config_dir: Path, dotfiles_dir: Path, profile: str, terminal: str
):
    """Write mock chezmoi config; back up and restore real config on exit."""
    config_file = config_dir / "chezmoi.toml"
    src = dotfiles_dir / ".github" / "test-data" / f"{profile}.toml"
    if not src.exists():
        print(f"ERROR: test-data config not found: {src}", file=sys.stderr)
        sys.exit(1)

    config_dir.mkdir(parents=True, exist_ok=True)

    is_isolated = Path("/.dockerenv").exists() or bool(os.environ.get("CI"))
    had_config = config_file.exists()
    backup_path: Path | None = None

    if not is_isolated and had_config:
        # Same directory = same filesystem, avoids cross-fs mv
        fd, bak = tempfile.mkstemp(
            prefix="chezmoi-backup-", suffix=".toml", dir=config_dir
        )
        os.close(fd)
        backup_path = Path(bak)
        shutil.copy2(config_file, backup_path)

    # Write and patch mock config
    shutil.copy2(src, config_file)
    _patch_terminal(config_file, terminal)

    try:
        yield
    finally:
        if not is_isolated:
            if had_config and backup_path:
                try:
                    shutil.move(str(backup_path), config_file)
                except Exception as e:
                    print(
                        f"WARNING: failed to restore {config_file}: {e}",
                        file=sys.stderr,
                    )
                    # Do NOT delete backup_path on failure — it's the last
                    # copy of the real config. Leave it for manual recovery.
            else:
                # No prior config existed — remove the mock so we don't leave
                # a phantom config behind (fixes M3)
                config_file.unlink(missing_ok=True)


def _patch_terminal(config_file: Path, terminal: str) -> None:
    """Override terminal value and recompute boolean flags in the config."""
    text = config_file.read_text()
    text = re.sub(r'terminal = .*', f'terminal = "{terminal}"', text)
    text = re.sub(
        r"isWezTerm = .*",
        f"isWezTerm = {str(terminal == 'wezterm').lower()}",
        text,
    )
    text = re.sub(
        r"isITerm2 = .*",
        f"isITerm2 = {str(terminal == 'iterm2').lower()}",
        text,
    )
    config_file.write_text(text)


# ---------------------------------------------------------------------------
# Template rendering helper
# ---------------------------------------------------------------------------


def test_template(tmpl_path: str, out_path: str, display_name: str) -> None:
    """Render a chezmoi template and record pass/fail."""
    label = (
        f"Template: {display_name} renders for "
        f"profile={PROFILE} terminal={TERMINAL}"
    )
    try:
        with open(tmpl_path, "r") as tmpl_file:
            result = run(
                "chezmoi",
                "execute-template",
                f"--source={DOTFILES_DIR}",
                stdin=tmpl_file,
            )
        if result.returncode == 0:
            Path(out_path).write_text(result.stdout)
            pass_test(label)
        else:
            fail_test(label, result.stderr)
    except Exception as e:
        fail_test(label, str(e))


# ---------------------------------------------------------------------------
# Category 1: Template rendering
# ---------------------------------------------------------------------------


def run_template_tests() -> None:
    print()
    print(f"=== Template Rendering (profile={PROFILE} terminal={TERMINAL}) ===")

    test_template(
        str(DOTFILES_DIR / "dot_config" / "starship.toml.tmpl"),
        "/tmp/ci-starship.toml",
        "starship.toml.tmpl",
    )

    test_template(
        str(DOTFILES_DIR / "dot_config" / "git" / "config.tmpl"),
        "/tmp/ci-git-config",
        "git/config.tmpl",
    )

    test_template(
        str(DOTFILES_DIR / "dot_wezterm.lua.tmpl"),
        "/tmp/ci-wezterm.lua",
        "dot_wezterm.lua.tmpl",
    )

    test_template(
        str(DOTFILES_DIR / "private_dot_env.tmpl"),
        "/tmp/ci-env",
        "private_dot_env.tmpl",
    )

    test_template(
        str(DOTFILES_DIR / "dot_config" / "1Password" / "ssh" / "agent.toml.tmpl"),
        "/tmp/ci-agent.toml",
        "1Password/ssh/agent.toml.tmpl",
    )

    test_template(
        str(
            DOTFILES_DIR
            / "dot_config"
            / "iterm2"
            / "DynamicProfiles"
            / "default.json.tmpl"
        ),
        "/tmp/ci-iterm2.json",
        "iterm2/DynamicProfiles/default.json.tmpl",
    )

    # .chezmoiscripts template(s) — both .sh.tmpl and .py.tmpl
    scripts_dir = DOTFILES_DIR / ".chezmoiscripts"
    for pattern in ("*.sh.tmpl", "*.py.tmpl"):
        for tmpl_script in sorted(scripts_dir.glob(pattern)):
            script_name = tmpl_script.name
            # Strip .tmpl suffix for the rendered output filename
            rendered_name = script_name.removesuffix(".tmpl")
            test_template(
                str(tmpl_script),
                f"/tmp/ci-script-{rendered_name}",
                f".chezmoiscripts/{script_name}",
            )


# ---------------------------------------------------------------------------
# Category 2: Syntax validation
# ---------------------------------------------------------------------------


def _validate_chezmoiexternal(external_yaml: Path) -> None:
    """Validate .chezmoiexternal.yaml syntax and field schema."""
    label = "Config: .chezmoiexternal.yaml is valid YAML"
    if not external_yaml.exists():
        pass_test(f"{label} (skipped — file not present)")
        return

    try:
        import yaml
    except ImportError:
        pass_test(f"{label} (skipped — pyyaml not installed)")
        return

    try:
        with open(external_yaml) as f:
            externals = yaml.safe_load(f)
        pass_test(label)
    except Exception as e:
        fail_test(label, str(e))
        return

    if not externals or not isinstance(externals, dict):
        return

    # Schema validation — catch invalid fields like the "recursive" bug
    VALID_GIT_REPO_FIELDS = {
        "type", "url", "clone", "pull", "refreshPeriod",
        "stripComponents", "include", "exclude", "encrypted",
        "filter", "readOnly",
    }
    VALID_ARCHIVE_FIELDS = VALID_GIT_REPO_FIELDS | {"format", "path"}
    VALID_FILE_FIELDS = {
        "type", "url", "refreshPeriod", "encrypted", "filter",
        "executable",
    }
    TYPE_FIELDS = {
        "git-repo": VALID_GIT_REPO_FIELDS,
        "archive": VALID_ARCHIVE_FIELDS,
        "archive-file": VALID_ARCHIVE_FIELDS,
        "file": VALID_FILE_FIELDS,
    }
    for target, spec in externals.items():
        ext_type = spec.get("type", "unknown")
        allowed = TYPE_FIELDS.get(ext_type)
        entry_label = f"Config: .chezmoiexternal.yaml '{target}' has valid fields for type '{ext_type}'"
        if allowed is None:
            fail_test(entry_label, f"Unknown external type: {ext_type}")
        else:
            invalid_fields = set(spec.keys()) - allowed
            if invalid_fields:
                fail_test(entry_label, f"Invalid fields: {invalid_fields}")
            else:
                pass_test(entry_label)


def run_syntax_tests() -> None:
    print()
    print("=== Syntax Validation ===")

    # TOML: starship.toml
    label = "Config: starship.toml is valid TOML"
    try:
        validate_toml("/tmp/ci-starship.toml")
        pass_test(label)
    except Exception as e:
        fail_test(label, str(e))

    # Git config syntax
    label = "Config: git/config is valid git config"
    result = run("git", "config", "--file", "/tmp/ci-git-config", "--list")
    if result.returncode == 0:
        pass_test(label)
    else:
        fail_test(label, result.stderr)

    # Regression: git config must not have duplicate [user] sections
    label = "Config: git/config has exactly 1 [user] section (no duplicates)"
    try:
        git_config_text = Path("/tmp/ci-git-config").read_text()
        user_count = len(re.findall(r"^\[user\]", git_config_text, re.MULTILINE))
        if user_count == 1:
            pass_test(label)
        else:
            fail_test(label, f"found {user_count} [user] sections, expected 1")
    except Exception as e:
        fail_test(label, str(e))

    # Regression: starship.toml must not have duplicate [directory] sections
    label = "Config: starship.toml has exactly 1 [directory] section (no duplicates)"
    try:
        starship_text = Path("/tmp/ci-starship.toml").read_text()
        dir_count = len(
            re.findall(r"^\[directory\]", starship_text, re.MULTILINE)
        )
        if dir_count == 1:
            pass_test(label)
        else:
            fail_test(label, f"found {dir_count} [directory] sections, expected 1")
    except Exception as e:
        fail_test(label, str(e))

    # Starship: validate that starship can actually parse the format string.
    # TOML validity (above) is not enough — starship has its own format parser
    # that rejects bad escapes (e.g. \\ line-endings) with "expected escaped_char".
    label = "Config: starship parses starship.toml format string without errors"
    if not shutil.which("starship"):
        pass_test(f"{label} (skipped — starship not installed)")
    else:
        env = {**os.environ, "STARSHIP_CONFIG": "/tmp/ci-starship.toml"}
        result = run("starship", "explain", env=env)
        if result.returncode == 0:
            pass_test(label)
        else:
            fail_test(label, result.stderr or result.stdout)

    # .chezmoiexternal.yaml — YAML validity + schema validation
    external_yaml = DOTFILES_DIR / ".chezmoiexternal.yaml"
    _validate_chezmoiexternal(external_yaml)

    # 1Password agent TOML
    label = "Config: 1Password/ssh/agent.toml is valid TOML"
    try:
        validate_toml("/tmp/ci-agent.toml")
        pass_test(label)
    except Exception as e:
        fail_test(label, str(e))

    # iterm2 JSON
    label = "Config: iterm2/DynamicProfiles/default.json is valid JSON"
    try:
        json.loads(Path("/tmp/ci-iterm2.json").read_text())
        pass_test(label)
    except Exception as e:
        fail_test(label, str(e))


# ---------------------------------------------------------------------------
# Category 3: Script linting
# ---------------------------------------------------------------------------


def run_lint_tests() -> None:
    print()
    print("=== Script Linting ===")

    scripts_dir = DOTFILES_DIR / ".chezmoiscripts"

    # Lint plain .sh scripts in .chezmoiscripts/
    for script in sorted(scripts_dir.glob("*.sh")):
        script_name = script.name
        label = f"Lint: .chezmoiscripts/{script_name} passes bash -n"
        result = run("bash", "-n", str(script))
        if result.returncode == 0:
            pass_test(label)
        else:
            fail_test(label, result.stderr)

    # Lint rendered .sh.tmpl scripts
    for tmpl_script in sorted(scripts_dir.glob("*.sh.tmpl")):
        script_name = tmpl_script.name
        rendered_name = script_name.removesuffix(".tmpl")
        rendered_file = Path(f"/tmp/ci-script-{rendered_name}")
        label = (
            f"Lint: .chezmoiscripts/{script_name} (rendered) passes bash -n"
        )
        if rendered_file.exists():
            result = run("bash", "-n", str(rendered_file))
            if result.returncode == 0:
                pass_test(label)
            else:
                fail_test(label, result.stderr)
        else:
            fail_test(
                label, "rendered file missing — template rendering must have failed"
            )

    # Lint shell scripts in dot_local/bin/
    bin_dir = DOTFILES_DIR / "dot_local" / "bin"
    for script in sorted(bin_dir.glob("executable_*")):
        if not script.is_file():
            continue
        # Check shebang for bash/sh
        try:
            first_line = script.read_text().split("\n", 1)[0]
        except Exception:
            continue
        if not re.search(r"#!/.*(?:bash|sh)", first_line):
            continue
        script_name = script.name
        label = f"Lint: dot_local/bin/{script_name} passes bash -n"
        result = run("bash", "-n", str(script))
        if result.returncode == 0:
            pass_test(label)
        else:
            fail_test(label, result.stderr)

    # Lint plain .py scripts in .chezmoiscripts/
    for script in sorted(scripts_dir.glob("*.py")):
        script_name = script.name
        label = f"Lint: .chezmoiscripts/{script_name} passes python3 -m py_compile"
        result = run("python3", "-m", "py_compile", str(script))
        if result.returncode == 0:
            pass_test(label)
        else:
            fail_test(label, result.stderr)

    # Lint rendered .py.tmpl scripts
    for tmpl_script in sorted(scripts_dir.glob("*.py.tmpl")):
        script_name = tmpl_script.name
        rendered_name = script_name.removesuffix(".tmpl")
        rendered_file = Path(f"/tmp/ci-script-{rendered_name}")
        label = f"Lint: .chezmoiscripts/{script_name} (rendered) passes python3 -m py_compile"
        if rendered_file.exists():
            result = run("python3", "-m", "py_compile", str(rendered_file))
            if result.returncode == 0:
                pass_test(label)
            else:
                fail_test(label, result.stderr)
        else:
            fail_test(
                label, "rendered file missing — template rendering must have failed"
            )

    # Lint the test script itself
    label = "Lint: tests/ci-test.py passes python3 -m py_compile"
    result = run("python3", "-m", "py_compile", str(Path(__file__).resolve()))
    if result.returncode == 0:
        pass_test(label)
    else:
        fail_test(label, result.stderr)


# ---------------------------------------------------------------------------
# Category 4: Hook tests (Python syntax + settings validation)
# ---------------------------------------------------------------------------


def run_hook_tests() -> None:
    print()
    print("=== Hook Tests ===")

    # Python syntax check for all hook scripts
    hooks_dir = DOTFILES_DIR / "dot_claude" / "hooks"
    py_files = sorted(hooks_dir.rglob("*.py"))
    for py_file in py_files:
        rel_name = str(py_file.relative_to(DOTFILES_DIR / "dot_claude"))
        label = f"Hook: {rel_name} passes Python syntax check"
        result = run("python3", "-m", "py_compile", str(py_file))
        if result.returncode == 0:
            pass_test(label)
        else:
            fail_test(label, result.stderr)

    # Determine settings file — may be .json or .json.tmpl
    settings_tmpl = DOTFILES_DIR / "dot_claude" / "settings.json.tmpl"
    settings_plain = DOTFILES_DIR / "dot_claude" / "settings.json"

    if settings_tmpl.exists():
        # Render the template first
        settings_path = Path("/tmp/ci-claude-settings.json")
        label = "Config: dot_claude/settings.json.tmpl renders successfully"
        try:
            with open(settings_tmpl, "r") as f:
                result = run(
                    "chezmoi",
                    "execute-template",
                    f"--source={DOTFILES_DIR}",
                    stdin=f,
                )
            if result.returncode == 0:
                settings_path.write_text(result.stdout)
                pass_test(label)
            else:
                fail_test(label, result.stderr)
                return  # Can't continue settings validation
        except Exception as e:
            fail_test(label, str(e))
            return
        settings_file = settings_path
        settings_display = "dot_claude/settings.json.tmpl (rendered)"
    elif settings_plain.exists():
        settings_file = settings_plain
        settings_display = "dot_claude/settings.json"
    else:
        fail_test("Config: dot_claude/settings.json not found")
        return

    # settings.json is valid JSON
    label = f"Config: {settings_display} is valid JSON"
    try:
        settings_data = json.loads(settings_file.read_text())
        pass_test(label)
    except Exception as e:
        fail_test(label, str(e))
        return  # Can't continue if JSON is invalid

    # Hook event names are valid Claude Code events
    VALID_EVENTS = {
        "Stop",
        "Notification",
        "SubagentStop",
        "SessionStart",
        "PreCompact",
        "PreToolUse",
        "PostToolUse",
        "UserPromptSubmit",
    }
    label = f"Config: {settings_display} hook events are all valid"
    hooks_data = settings_data.get("hooks", {})
    invalid = set(hooks_data.keys()) - VALID_EVENTS
    if not invalid:
        pass_test(label)
    else:
        fail_test(label, f"Invalid hook events: {invalid}")

    # Hook commands reference scripts that exist in the repo
    label = f"Config: {settings_display} hook commands reference existing scripts"
    missing = []
    for hooks_list in hooks_data.values():
        for matcher in hooks_list:
            for hook in matcher.get("hooks", []):
                cmd = hook.get("command", "")
                # Use a portable pattern — home dir varies by OS/user
                m = re.search(r"\.claude/hooks/(\S+\.py)", cmd)
                if m:
                    name = m.group(1)
                    # chezmoi strips "executable_" prefix on deploy; check both forms
                    rel = "dot_claude/hooks/" + name
                    rel_exec = "dot_claude/hooks/executable_" + name
                    if not (DOTFILES_DIR / rel).exists() and not (DOTFILES_DIR / rel_exec).exists():
                        missing.append(rel)
    if not missing:
        pass_test(label)
    else:
        fail_test(label, "Missing hook scripts:\n" + "\n".join(missing))


# ---------------------------------------------------------------------------
# Category 5: Hook unit tests (pytest)
# ---------------------------------------------------------------------------


def run_hook_unit_tests() -> None:
    print()
    print("=== Hook Unit Tests ===")

    test_file = DOTFILES_DIR / "tests" / "test_hooks.py"
    label = "Hook unit tests (pytest)"
    if not test_file.exists():
        fail_test(label, f"test file not found: {test_file}")
        return

    result = run(
        "python3", "-m", "pytest", str(test_file), "-v",
        cwd=str(DOTFILES_DIR),
    )
    if result.returncode == 0:
        pass_test(label)
    else:
        fail_test(label, result.stdout + "\n" + result.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    config_dir = (
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "chezmoi"
    )

    print("chezmoi dotfiles CI tests")
    print(f"  PROFILE:      {PROFILE}")
    print(f"  TERMINAL:     {TERMINAL}")
    print(f"  DOTFILES_DIR: {DOTFILES_DIR}")

    with chezmoi_config(config_dir, DOTFILES_DIR, PROFILE, TERMINAL):
        run_template_tests()
        run_syntax_tests()
        run_lint_tests()
        run_hook_tests()
        run_hook_unit_tests()

    print()
    print("=" * 40)
    total = PASS_COUNT + FAIL_COUNT
    print(f"RESULTS: {PASS_COUNT}/{total} passed, {FAIL_COUNT} failed")
    print("=" * 40)

    sys.exit(1 if FAIL_COUNT > 0 else 0)


if __name__ == "__main__":
    main()
