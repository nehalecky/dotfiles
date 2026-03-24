#!/bin/bash
# Install Claude Code plugins and register marketplaces
#
# Reads ~/.claude/plugin-marketplaces.json for marketplace definitions
# and ~/.claude/settings.json for enabled plugins, then ensures all
# referenced marketplaces are registered and plugins are installed.
#
# Requires: python3, claude CLI
# Idempotent: safe to run multiple times

set -euo pipefail

PLUGIN_MARKETPLACES="$HOME/.claude/plugin-marketplaces.json"
SETTINGS="$HOME/.claude/settings.json"
INSTALLED_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
warn() { echo "  [warn] $*" >&2; }
info() { echo "  [plugin-setup] $*"; }

# -------------------------------------------------------------------
# Pre-flight checks
# -------------------------------------------------------------------
if ! command -v claude &>/dev/null; then
  info "claude CLI not found -- skipping plugin setup"
  exit 0
fi

if [[ ! -f "$SETTINGS" ]]; then
  info "No settings.json found at $SETTINGS -- skipping plugin setup"
  exit 0
fi

if [[ ! -f "$PLUGIN_MARKETPLACES" ]]; then
  info "No plugin-marketplaces.json found at $PLUGIN_MARKETPLACES -- skipping plugin setup"
  exit 0
fi

# -------------------------------------------------------------------
# Parse marketplace map and enabled plugins using python3
# -------------------------------------------------------------------
# Outputs two sections separated by "---":
#   1. marketplace_name|github_repo  (from plugin-marketplaces.json)
#   2. plugin_name|marketplace_name  (non-official from settings.json)
read_config() {
  python3 - "$PLUGIN_MARKETPLACES" "$SETTINGS" "$INSTALLED_PLUGINS" <<'PYEOF'
import json, sys, os

mp_file, settings_file, installed_file = sys.argv[1], sys.argv[2], sys.argv[3]

# Load marketplace definitions
with open(mp_file) as f:
    marketplaces = json.load(f)

# Load enabled plugins from settings
with open(settings_file) as f:
    settings = json.load(f)

enabled = settings.get("enabledPlugins", {})

# Load already-installed plugins (for idempotency)
installed = set()
if os.path.isfile(installed_file):
    with open(installed_file) as f:
        data = json.load(f)
    for key in data.get("plugins", {}):
        installed.add(key)

# Section 1: marketplace definitions
for name, info in marketplaces.items():
    print(f"MARKETPLACE|{name}|{info['repo']}")

# Section 2: non-official enabled plugins
for plugin_key, enabled_val in enabled.items():
    if not enabled_val:
        continue
    if "@" not in plugin_key:
        continue
    plugin_name, marketplace = plugin_key.rsplit("@", 1)
    if marketplace == "claude-plugins-official":
        continue

    already_installed = plugin_key in installed
    has_marketplace_def = marketplace in marketplaces
    print(f"PLUGIN|{plugin_name}|{marketplace}|{'true' if already_installed else 'false'}|{'true' if has_marketplace_def else 'false'}")
PYEOF
}

config_output=$(read_config)

# -------------------------------------------------------------------
# Register marketplaces
# -------------------------------------------------------------------
info "Checking marketplace registrations..."

while IFS='|' read -r type name repo; do
  [[ "$type" != "MARKETPLACE" ]] && continue

  # Check if already registered
  if claude plugin marketplace list 2>/dev/null | grep -qF "$name"; then
    info "Marketplace '$name' already registered"
  else
    info "Registering marketplace '$name' from $repo..."
    claude plugin marketplace add "$repo" || warn "Failed to register marketplace '$name' ($repo)"
  fi
done <<< "$config_output"

# -------------------------------------------------------------------
# Install plugins
# -------------------------------------------------------------------
info "Checking plugin installations..."

while IFS='|' read -r type plugin_name marketplace already_installed has_marketplace_def; do
  [[ "$type" != "PLUGIN" ]] && continue

  plugin_key="${plugin_name}@${marketplace}"

  # Warn if marketplace not defined in our config
  if [[ "$has_marketplace_def" == "false" ]]; then
    warn "Plugin '$plugin_key' references marketplace '$marketplace' which is not in plugin-marketplaces.json"
    continue
  fi

  # Skip if already installed
  if [[ "$already_installed" == "true" ]]; then
    info "Plugin '$plugin_key' already installed"
    continue
  fi

  info "Installing plugin '$plugin_key'..."
  claude plugin install "$plugin_key" --scope user || warn "Failed to install plugin '$plugin_key'"
done <<< "$config_output"

info "Plugin setup complete."
