#!/usr/bin/env bash
# CI test script for chezmoi dotfiles repository
# Tests template rendering, syntax validation, and script linting
# Usage: PROFILE=personal TERMINAL=wezterm bash tests/ci-test.sh

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROFILE="${PROFILE:-personal}"
TERMINAL="${TERMINAL:-wezterm}"
DOTFILES_DIR="${DOTFILES_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

# Colors (only when stdout is a terminal)
if [[ -t 1 ]]; then
  GREEN='\033[0;32m'
  RED='\033[0;31m'
  RESET='\033[0m'
else
  GREEN=''
  RED=''
  RESET=''
fi

PASS_COUNT=0
FAIL_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf "${GREEN}[PASS]${RESET} %s\n" "$1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf "${RED}[FAIL]${RESET} %s\n" "$1"
}

# Detect sed flavor once at startup (avoid forking on every call)
if sed --version &>/dev/null 2>&1; then
  SED_INPLACE=(sed -i)
else
  SED_INPLACE=(sed -i '')
fi

# Validate a TOML file using Python's tomllib (3.11+) or tomli fallback
validate_toml() {
  local file="$1"
  python3 -c "
import sys
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print('ERROR: no tomllib/tomli available', file=sys.stderr)
        sys.exit(1)
with open(sys.argv[1], 'rb') as f:
    tomllib.load(f)
" "$file"
}

# Render a chezmoi template and test it
test_template() {
  local tmpl_path="$1"
  local out_path="$2"
  local display_name="$3"
  local label="Template: ${display_name} renders for profile=${PROFILE} terminal=${TERMINAL}"
  if chezmoi execute-template --source="$DOTFILES_DIR" \
       < "$tmpl_path" > "$out_path" 2>/tmp/ci-tmpl-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-tmpl-err >&2
  fi
}

# ---------------------------------------------------------------------------
# Setup: write mock chezmoi config
# ---------------------------------------------------------------------------

setup_config() {
  local config_dir
  config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/chezmoi"
  mkdir -p "$config_dir"

  local src_config="$DOTFILES_DIR/.github/test-data/${PROFILE}.toml"
  if [[ ! -f "$src_config" ]]; then
    echo "ERROR: test-data config not found: $src_config" >&2
    exit 1
  fi

  cp "$src_config" "$config_dir/chezmoi.toml"

  # Override terminal value and recompute boolean flags in a single sed pass
  local is_wezterm="false" is_iterm2="false"
  case "$TERMINAL" in
    wezterm) is_wezterm="true" ;;
    iterm2)  is_iterm2="true" ;;
  esac

  "${SED_INPLACE[@]}" \
    -e "s/terminal = .*/terminal = \"$TERMINAL\"/" \
    -e "s/isWezTerm = .*/isWezTerm = $is_wezterm/" \
    -e "s/isITerm2 = .*/isITerm2 = $is_iterm2/" \
    "$config_dir/chezmoi.toml"
}

# ---------------------------------------------------------------------------
# Category 1: Template rendering
# ---------------------------------------------------------------------------

run_template_tests() {
  echo ""
  echo "=== Template Rendering (profile=${PROFILE} terminal=${TERMINAL}) ==="

  test_template "$DOTFILES_DIR/dot_config/starship.toml.tmpl" \
    /tmp/ci-starship.toml "starship.toml.tmpl"

  test_template "$DOTFILES_DIR/dot_config/git/config.tmpl" \
    /tmp/ci-git-config "git/config.tmpl"

  test_template "$DOTFILES_DIR/dot_wezterm.lua.tmpl" \
    /tmp/ci-wezterm.lua "dot_wezterm.lua.tmpl"

  test_template "$DOTFILES_DIR/private_dot_env.tmpl" \
    /tmp/ci-env "private_dot_env.tmpl"

  test_template "$DOTFILES_DIR/dot_config/1Password/ssh/agent.toml.tmpl" \
    /tmp/ci-agent.toml "1Password/ssh/agent.toml.tmpl"

  test_template "$DOTFILES_DIR/dot_config/iterm2/DynamicProfiles/default.json.tmpl" \
    /tmp/ci-iterm2.json "iterm2/DynamicProfiles/default.json.tmpl"

  # .chezmoiscripts template(s)
  for tmpl_script in "$DOTFILES_DIR"/.chezmoiscripts/*.sh.tmpl; do
    [[ -f "$tmpl_script" ]] || continue
    local script_name
    script_name="$(basename "$tmpl_script")"
    test_template "$tmpl_script" \
      "/tmp/ci-script-${script_name%.tmpl}" ".chezmoiscripts/${script_name}"
  done
}

# ---------------------------------------------------------------------------
# Category 2: Syntax validation
# ---------------------------------------------------------------------------

run_syntax_tests() {
  echo ""
  echo "=== Syntax Validation ==="

  local label

  # TOML: starship.toml
  label="Config: starship.toml is valid TOML"
  if validate_toml /tmp/ci-starship.toml 2>/tmp/ci-syn-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-syn-err >&2
  fi

  # Git config syntax
  label="Config: git/config is valid git config"
  if git config --file /tmp/ci-git-config --list > /dev/null 2>/tmp/ci-syn-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-syn-err >&2
  fi

  # Regression: git config must not have duplicate [user] sections
  label="Config: git/config has exactly 1 [user] section (no duplicates)"
  local user_count
  user_count=$(grep -c '^\[user\]' /tmp/ci-git-config || true)
  if [[ "$user_count" -eq 1 ]]; then
    pass "$label"
  else
    fail "$label (found ${user_count} [user] sections, expected 1)"
  fi

  # Regression: starship.toml must not have duplicate [directory] sections (issue #4)
  label="Config: starship.toml has exactly 1 [directory] section (no duplicates)"
  local dir_count
  dir_count=$(grep -c '^\[directory\]' /tmp/ci-starship.toml || true)
  if [[ "$dir_count" -eq 1 ]]; then
    pass "$label"
  else
    fail "$label (found ${dir_count} [directory] sections, expected 1)"
  fi

  # 1Password agent TOML
  label="Config: 1Password/ssh/agent.toml is valid TOML"
  if validate_toml /tmp/ci-agent.toml 2>/tmp/ci-syn-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-syn-err >&2
  fi

  # iterm2 JSON
  label="Config: iterm2/DynamicProfiles/default.json is valid JSON"
  if python3 -c "import json, sys; json.load(open(sys.argv[1]))" /tmp/ci-iterm2.json 2>/tmp/ci-syn-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-syn-err >&2
  fi
}

# ---------------------------------------------------------------------------
# Category 3: Script linting
# ---------------------------------------------------------------------------

run_lint_tests() {
  echo ""
  echo "=== Script Linting ==="

  local label

  # Lint plain .sh scripts in .chezmoiscripts/
  for script in "$DOTFILES_DIR"/.chezmoiscripts/*.sh; do
    [[ -f "$script" ]] || continue
    local script_name
    script_name="$(basename "$script")"
    label="Lint: .chezmoiscripts/${script_name} passes bash -n"
    if bash -n "$script" 2>/tmp/ci-lint-err; then
      pass "$label"
    else
      fail "$label"
      cat /tmp/ci-lint-err >&2
    fi
  done

  # Lint rendered .sh.tmpl scripts
  for tmpl_script in "$DOTFILES_DIR"/.chezmoiscripts/*.sh.tmpl; do
    [[ -f "$tmpl_script" ]] || continue
    local script_name
    script_name="$(basename "$tmpl_script")"
    local rendered_file="/tmp/ci-script-${script_name%.tmpl}"
    label="Lint: .chezmoiscripts/${script_name} (rendered) passes bash -n"
    if [[ -f "$rendered_file" ]]; then
      if bash -n "$rendered_file" 2>/tmp/ci-lint-err; then
        pass "$label"
      else
        fail "$label"
        cat /tmp/ci-lint-err >&2
      fi
    else
      fail "$label (rendered file missing — template rendering must have failed)"
    fi
  done

  # Lint shell scripts in dot_local/bin/
  for script in "$DOTFILES_DIR"/dot_local/bin/executable_*; do
    [[ -f "$script" ]] || continue
    head -1 "$script" | grep -qE '#!/.*bash|#!/.*sh' || continue
    local script_name
    script_name="$(basename "$script")"
    label="Lint: dot_local/bin/${script_name} passes bash -n"
    if bash -n "$script" 2>/tmp/ci-lint-err; then
      pass "$label"
    else
      fail "$label"
      cat /tmp/ci-lint-err >&2
    fi
  done

  # Lint the test script itself
  label="Lint: tests/ci-test.sh passes bash -n"
  if bash -n "${BASH_SOURCE[0]}" 2>/tmp/ci-lint-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-lint-err >&2
  fi
}

# ---------------------------------------------------------------------------
# Category 4: Hook tests (Python syntax + settings validation)
# ---------------------------------------------------------------------------

run_hook_tests() {
  echo ""
  echo "=== Hook Tests ==="

  local label

  # Python syntax check for all hook scripts
  for py_file in \
    "$DOTFILES_DIR"/dot_claude/hooks/*.py \
    "$DOTFILES_DIR"/dot_claude/hooks/utils/llm/*.py \
    "$DOTFILES_DIR"/dot_claude/hooks/utils/tts/*.py; do
    [[ -f "$py_file" ]] || continue
    local rel_name
    rel_name="${py_file#$DOTFILES_DIR/dot_claude/}"
    label="Hook: ${rel_name} passes Python syntax check"
    if python3 -m py_compile "$py_file" 2>/tmp/ci-hook-err; then
      pass "$label"
    else
      fail "$label"
      cat /tmp/ci-hook-err >&2
    fi
  done

  # settings.json is valid JSON
  local settings="$DOTFILES_DIR/dot_claude/settings.json"
  label="Config: dot_claude/settings.json is valid JSON"
  if python3 -c "import json, sys; json.load(open(sys.argv[1]))" \
       "$settings" 2>/tmp/ci-hook-err; then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-hook-err >&2
  fi

  # settings.json hook event names are valid Claude Code events
  label="Config: dot_claude/settings.json hook events are all valid"
  if python3 - "$settings" 2>/tmp/ci-hook-err <<'PYEOF'
import json, sys
VALID = {"Stop","Notification","SubagentStop","SessionStart",
         "PreCompact","PreToolUse","PostToolUse","UserPromptSubmit"}
data = json.load(open(sys.argv[1]))
invalid = set(data.get("hooks", {}).keys()) - VALID
if invalid:
    print(f"Invalid hook events: {invalid}", file=sys.stderr)
    sys.exit(1)
PYEOF
  then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-hook-err >&2
  fi

  # settings.json hook commands reference scripts that exist in the repo
  label="Config: dot_claude/settings.json hook commands reference existing scripts"
  if python3 - "$settings" "$DOTFILES_DIR" 2>/tmp/ci-hook-err <<'PYEOF'
import json, sys, re
from pathlib import Path
data = json.load(open(sys.argv[1]))
dotfiles = Path(sys.argv[2])
missing = []
for hooks_list in data.get("hooks", {}).values():
    for matcher in hooks_list:
        for hook in matcher.get("hooks", []):
            cmd = hook.get("command", "")
            m = re.search(r'/Users/\S+/\.claude/hooks/(\S+\.py)', cmd)
            if m:
                rel = "dot_claude/hooks/" + m.group(1)
                if not (dotfiles / rel).exists():
                    missing.append(rel)
if missing:
    print("Missing hook scripts:\n" + "\n".join(missing), file=sys.stderr)
    sys.exit(1)
PYEOF
  then
    pass "$label"
  else
    fail "$label"
    cat /tmp/ci-hook-err >&2
  fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "chezmoi dotfiles CI tests"
echo "  PROFILE:      ${PROFILE}"
echo "  TERMINAL:     ${TERMINAL}"
echo "  DOTFILES_DIR: ${DOTFILES_DIR}"

setup_config
run_template_tests
run_syntax_tests
run_lint_tests
run_hook_tests

echo ""
echo "========================================"
TOTAL=$((PASS_COUNT + FAIL_COUNT))
echo "RESULTS: ${PASS_COUNT}/${TOTAL} passed, ${FAIL_COUNT} failed"
echo "========================================"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi
exit 0
