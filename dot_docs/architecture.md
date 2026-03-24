# Dotfiles Architecture

## Overview

This repository uses [chezmoi](https://chezmoi.io) to manage dotfiles across two machine profiles
(`personal` and `work`). The central design principle is **init-time identity injection**: `chezmoi init`
captures machine identity (name, email, SSH keys, 1Password vault items) once and stores it in a
local config file that is never committed. All profile-specific behavior flows from that single
init decision.

---

## Data Flow

### Init-Time Identity Injection

```
chezmoi init https://github.com/<your-github-username>/dotfiles.git
    |
    v
.chezmoi.toml.tmpl
    Prompts (captured once via promptStringOnce / promptChoiceOnce):
      - profile        ("personal" | "work")
      - git_name       (full name)
      - preferred_name (casual name, defaults to first word of git_name)
      - git_email      (profile-defaulted)
      - github_username
      - git_signing_key  (SSH public key, ed25519)
      - op_auth_key_name    (1Password item name for SSH auth key)
      - op_signing_key_name (1Password item name for signing key)
    |
    v
~/.config/chezmoi/chezmoi.toml   <-- LOCAL ONLY, never committed
    [data] section with all identity values resolved
    |
    v
chezmoi apply
    |
    +-- .chezmoidata.yaml  (behavioral defaults, committed)
    |     starship.* settings, no identity data
    |
    +-- chezmoi.toml [data] (identity overrides, local)
    |
    v
Template variables available in all *.tmpl files:
  .profile            "personal" | "work"
  .isPersonal         bool
  .isWork             bool
  .git_name           string
  .preferred_name     string
  .git_email          string
  .github_username    string
  .git_signing_key    SSH public key string
  .op_auth_key_name   1Password item name
  .op_signing_key_name 1Password item name
  .chezmoi.homeDir    $HOME (chezmoi built-in)
  .chezmoi.os         "darwin" | "linux" (chezmoi built-in)
  .starship.*         from .chezmoidata.yaml
    |
    v
*.tmpl files rendered  ->  deployed to $HOME
.chezmoiignore evaluated ->  files excluded per profile
run_onchange_* scripts  ->  executed when content hash changes
run_once_* scripts      ->  executed once per machine
```

### Apply-Time: Two Data Sources

Template rendering merges two sources, with `chezmoi.toml` taking precedence:

```
.chezmoidata.yaml          chezmoi.toml [data]
(committed defaults)       (local identity, never committed)
        |                          |
        +----------+----------+----+
                   |
                   v
           Template variables
```

This separation keeps behavioral defaults version-controlled and identity data machine-local.

---

## Source Tree

```
~/.local/share/chezmoi/                  # The git repository
|
|-- .chezmoi.toml.tmpl                   # Init-time prompt definitions
|-- .chezmoidata.yaml                    # Behavioral defaults (starship settings)
|-- .chezmoiignore                       # Profile-conditional file exclusions
|-- .gitignore                           # Repo-internal ignore rules
|
|-- .chezmoiscripts/
|   |-- run_once_install-homebrew.sh     # Bootstrap Homebrew (once)
|   |-- run_onchange_after_20-brew-bundle.sh.tmpl  # brew bundle (on Brewfile change)
|   |-- run_onchange_install-starship.sh.tmpl       # Install starship (on change)
|   `-- run_once_after_40-starship-check.sh         # Verify starship post-install
|
|-- dot_Brewfile.tmpl                    # Profile-aware package manifest -> ~/.Brewfile
|-- dot_wezterm.lua.tmpl                 # WezTerm config with profile theming -> ~/.wezterm.lua
|-- dot_zshrc                            # Zsh interactive config -> ~/.zshrc
|-- dot_zshenv                           # Zsh environment (always sourced) -> ~/.zshenv
|-- dot_zprofile                         # Zsh login profile -> ~/.zprofile
|-- dot_zlogin                           # Zsh post-login -> ~/.zlogin
|-- dot_zlogout                          # Zsh logout -> ~/.zlogout
|-- dot_zpreztorc                        # Prezto configuration -> ~/.zpreztorc
|-- dot_bashrc                           # Bash config (fallback) -> ~/.bashrc
|-- dot_gitignore                        # Global gitignore -> ~/.gitignore
|-- dot_taskrc                           # Taskwarrior config -> ~/.taskrc
|-- symlink_dot_git                      # Symlink: ~/.git -> chezmoi source
|
|-- private_dot_env.tmpl                 # Environment variables (600 perms) -> ~/.env
|-- private_dot_gitconfig                # Git config (600 perms) -> ~/.gitconfig
|
|-- private_dot_ssh/
|   |-- private_config                   # SSH client config (600 perms) -> ~/.ssh/config
|   |-- allowed_signers.tmpl             # SSH signing allowlist -> ~/.ssh/allowed_signers
|   `-- id_ed25519_signing.pub           # Signing public key (personal only)
|
|-- dot_claude/                          # Claude Code configuration -> ~/.claude/
|   |-- agents/                          # Specialized sub-agents
|   |-- commands/                        # Custom slash commands
|   |-- hooks/                           # Python workflow automation hooks
|   |-- memories/                        # Project context and methodology files
|   |   `-- personal/user-info.md.tmpl   # Identity-aware memory template
|   |-- output-styles/                   # Response formatting styles
|   |-- status_lines/                    # Status bar configurations
|   |-- settings.json                    # Global Claude settings
|   |-- settings.framework.json          # Framework variant settings
|   |-- settings.minimal.json            # Minimal variant settings
|   `-- settings.production.json         # Production variant settings
|
|-- dot_config/
|   |-- 1Password/ssh/agent.toml.tmpl    # SSH agent key list -> ~/.config/1Password/ssh/agent.toml
|   |-- git/config.tmpl                  # Git identity config -> ~/.config/git/config
|   |-- starship.toml.tmpl               # Starship prompt (profile-conditional) -> ~/.config/starship.toml
|   |-- iterm2/DynamicProfiles/
|   |   `-- default.json.tmpl            # iTerm2 profile (work badge) -> ~/.config/iterm2/...
|   |-- exact_starship/themes/           # Additional starship theme files
|   |-- conda/condarc                    # Conda configuration
|   |-- doom/                            # Doom Emacs configuration
|   |-- lazygit/config.yml               # Lazygit configuration
|   |-- shell/xdg-env.sh                 # XDG environment variable definitions
|   |-- weechat/                         # WeeChat IRC configuration (private_*)
|   |-- yazi/                            # Yazi file manager configuration
|   `-- zed/                             # Zed editor configuration
|
|-- dot_local/bin/                       # User scripts -> ~/.local/bin/
|   |-- executable_claude-sessions       # Claude session management
|   |-- executable_doc                   # Documentation browser
|   |-- executable_glow-handler          # Glow markdown viewer helper
|   |-- executable_sync-secrets          # Secrets synchronization
|   |-- executable_weather / weather-display
|   |-- executable_wezterm-shortcuts     # WezTerm keybinding reference
|   |-- executable_workspace-dev         # Development workspace launcher (zellij)
|   `-- executable_workspace-home        # Home command center launcher (zellij)
|
|-- dot_docs/                            # Documentation -> ~/.docs/
|-- dot_task/hooks/                      # Taskwarrior hooks
|-- dot_vscode/settings.json             # VS Code settings -> ~/.vscode/settings.json
`-- exact_dot_scripts/                   # Shell scripts -> ~/.scripts/ (exact sync)
```

---

## Profile System

Two profiles exist. The profile chosen at `chezmoi init` gates identity, packages, terminal
theming, and file inclusion throughout the repository.

### Profile Comparison

| Component              | personal                           | work                                  |
|------------------------|------------------------------------|---------------------------------------|
| Git email              | `<git_email prompt default>`       | user@company.com                      |
| Git signing key        | personal ed25519 key               | work ed25519 key                      |
| 1Password auth key     | "GitHub SSH Auth Key"              | "GitHub Auth Key"                     |
| 1Password signing key  | "Git Commit Signing Key"           | "Signing Key"                         |
| Brewfile extras        | Signal, Spotify, Steam, Telegram   | cosign, k9s, kubectl, helm, Docker, Slack, Zoom |
| Starship prompt        | Minimal; k8s/aws/gcloud disabled   | k8s context, AWS profile/region, hostname, bold colors |
| WezTerm tab bar        | Default dark theme                 | Muted red tab bar + "WORK" right-status badge |
| iTerm2 profile         | No badge                           | "WORK" badge, red-tinted              |
| SSH allowed_signers    | Personal key                       | Work key                              |
| 1Password agent.toml   | Personal vault key items           | Work vault key items                  |
| .chezmoiignore         | Excludes .kube/, .aws/             | Excludes id_ed25519_signing.pub       |
| Claude user-info.md    | Personal identity context          | Work identity context                 |

### Profile-Conditional .chezmoiignore

`.chezmoiignore` evaluates template logic at apply time:

```
{{ if .isWork }}
.ssh/id_ed25519_signing.pub   # personal signing pubkey not deployed to work machines
{{ end }}

{{ if .isPersonal }}
.kube/                        # kubernetes config excluded on personal machines
.aws/                         # AWS config excluded on personal machines
{{ end }}
```

---

## Template Files

Chezmoi renders all `.tmpl` files at apply time. Identity variables come from `chezmoi.toml`;
behavioral variables come from `.chezmoidata.yaml`.

| Source file                                     | Deployed to                              | What it parameterizes                                       |
|-------------------------------------------------|------------------------------------------|-------------------------------------------------------------|
| `.chezmoi.toml.tmpl`                            | `~/.config/chezmoi/chezmoi.toml`         | Init prompts only; sets all identity variables              |
| `dot_Brewfile.tmpl`                             | `~/.Brewfile`                            | `.isWork` / `.isPersonal` gates package sections            |
| `dot_wezterm.lua.tmpl`                          | `~/.wezterm.lua`                         | `.profile` for tab bar color and right-status WORK badge    |
| `dot_config/git/config.tmpl`                    | `~/.config/git/config`                   | `.git_name`, `.git_email`, `.git_signing_key`, `homeDir`    |
| `dot_config/starship.toml.tmpl`                 | `~/.config/starship.toml`                | `.profile` for k8s/aws modules and color theme              |
| `dot_config/1Password/ssh/agent.toml.tmpl`      | `~/.config/1Password/ssh/agent.toml`     | `.op_auth_key_name`, `.op_signing_key_name`                 |
| `dot_config/iterm2/DynamicProfiles/default.json.tmpl` | `~/.config/iterm2/DynamicProfiles/default.json` | `.isWork` for WORK badge                         |
| `private_dot_env.tmpl`                          | `~/.env` (mode 600)                      | Placeholder for `onepasswordRead` API token injection       |
| `private_dot_ssh/allowed_signers.tmpl`          | `~/.ssh/allowed_signers`                 | `.git_email`, `.git_signing_key` for SSH commit verification |
| `dot_claude/memories/personal/user-info.md.tmpl`| `~/.claude/memories/personal/user-info.md` | Identity context for Claude Code agent memory             |
| `.chezmoiscripts/run_onchange_after_20-brew-bundle.sh.tmpl` | (executed, not deployed)   | Includes Brewfile hash to trigger re-run on content change  |
| `.chezmoiscripts/run_onchange_install-starship.sh.tmpl`     | (executed, not deployed)   | `.chezmoi.os` for OS-conditional install path               |

---

## Secret Management

This repository contains no encrypted secrets store. Secret access relies on two mechanisms:

### 1Password SSH Agent

SSH keys (auth and signing) live in 1Password. The 1Password SSH agent socket serves them to
the system. The `agent.toml` template controls which vault items to offer:

```toml
# ~/.config/1Password/ssh/agent.toml (rendered from template)
[[ssh-keys]]
item = "GitHub SSH Auth Key"   # value from .op_auth_key_name

[[ssh-keys]]
item = "Git Commit Signing Key"  # value from .op_signing_key_name
```

Git signs commits through the 1Password `op-ssh-sign` binary:

```
[gpg "ssh"]
    program = "/Applications/1Password.app/Contents/MacOS/op-ssh-sign"
    allowedSignersFile = ~/.ssh/allowed_signers
```

No private key material exists in the repository or in `~/.ssh/`.

### Environment Variable Templating

`private_dot_env.tmpl` (deployed as `~/.env`, mode 600) holds `onepasswordRead` calls that inject
API tokens at apply time. It currently contains only commented examples. Entries follow this pattern:

```bash
export GITHUB_TOKEN='{{ onepasswordRead "op://Private/github-pat/token" }}'
```

The `private_` prefix tells chezmoi to deploy the file with mode 600.

### What Does Not Exist

- No `.secrets/` directory
- No Age encryption
- No GPG-encrypted files
- No `.1password/` directory in source

---

## Automation Scripts

### run_once vs run_onchange

Chezmoi distinguishes two script types:

- `run_once_*` -- runs once per machine, tracked by script name in chezmoi state
- `run_onchange_*` -- runs whenever script content changes (re-evaluated each apply)

| Script                                       | Type         | Trigger                          | Purpose                              |
|----------------------------------------------|--------------|----------------------------------|--------------------------------------|
| `run_once_install-homebrew.sh`               | run_once     | First apply on new machine       | Bootstrap Homebrew                   |
| `run_onchange_after_20-brew-bundle.sh.tmpl`  | run_onchange | Brewfile content hash changes    | Run `brew bundle --global`           |
| `run_onchange_install-starship.sh.tmpl`      | run_onchange | Script content changes           | Install starship via brew or curl    |
| `run_once_after_40-starship-check.sh`        | run_once     | After other run_once scripts     | Verify starship installation         |

The brew-bundle script uses a content-hash trick to couple its trigger to Brewfile changes:

```bash
#!/bin/bash
# Brewfile hash: {{ include "dot_Brewfile.tmpl" | sha256sum }}
```

Embedding the Brewfile hash in the script body causes chezmoi to detect a content change and
re-execute the script whenever the Brewfile changes.

---

## Claude Code Hooks

The `dot_claude/hooks/` directory contains a Python-based notification system driven by Claude
Code's lifecycle hooks. Three hook scripts (`stop.py`, `subagent_stop.py`, `notification.py`) fire
on session events, log structured JSON, and optionally announce completions or input requests via
speech synthesis.

The system uses a priority-chain architecture: multiple TTS backends (ElevenLabs, OpenAI, Kokoro,
pyttsx3/macOS say) and LLM backends (claude_cli, OpenAI, Anthropic, Ollama) are tried in quality
order, falling through on unavailability. A recursion guard (`_CLAUDE_HOOK_GENERATING=1`) prevents
infinite loops when the `claude_cli` backend invokes `claude -p`.

All hooks exit 0 unconditionally -- a failed notification never blocks a Claude session.

For full architecture diagrams, backend details, configuration reference, and extensibility guide,
see [Claude Code Hooks](claude-hooks.md).

---

## Design Decisions

### Templates Over Branches

A single branch handles both profiles through template conditionals rather than maintaining
separate `personal` and `work` branches. This approach:

- Keeps one commit history with no divergence
- Makes profile differences explicit and auditable in source
- Requires one edit for new profile-conditional behavior, not a branch merge

### promptStringOnce / promptChoiceOnce

Init prompts use the `Once` variants, which store answers in `chezmoi.toml` after the first run.
Subsequent `chezmoi apply` calls reuse stored values without re-prompting, making apply idempotent
and safe to run frequently.

### run_onchange for Brew Bundle

The brew-bundle script uses `run_onchange` rather than `run_once`, so new Brewfile packages
install on existing machines, not only new ones. The sha256 hash injection in the script body
couples the trigger to Brewfile content.

### Lua-Native Profile Logic in WezTerm

The WezTerm config (`dot_wezterm.lua.tmpl`) injects only the profile string
(`local chezmoi_profile = "{{ .profile }}"`). All conditional logic (tab bar colors, status badge)
lives in Lua rather than template conditionals. This approach:

- Keeps the deployed `.wezterm.lua` valid Lua regardless of profile
- Lets WezTerm reload configuration at runtime without a chezmoi re-apply
- Centralizes profile-conditional logic in one readable file

### private_ Prefix for Permissions

Chezmoi deploys files prefixed with `private_` at mode 600. This applies to:

- `~/.env` — environment variables may include API tokens
- `~/.gitconfig` — contains email and signing key identity
- `~/.ssh/config` — SSH client configuration
- `~/.config/weechat/*.conf` — IRC credentials

### XDG Base Directory Compliance

Configuration follows the XDG Base Directory specification where tools support it. Examples:

- `~/.config/git/config` (not `~/.gitconfig` as primary)
- `~/.config/starship.toml`
- `~/.config/lazygit/config.yml`
- `~/.local/bin/` for user scripts

`~/.gitconfig` exists as a `private_` file for tools that ignore XDG.

---

## Key File Locations

| Purpose                         | Source path                                  | Deployed path                              |
|---------------------------------|----------------------------------------------|--------------------------------------------|
| Init prompts                    | `.chezmoi.toml.tmpl`                         | `~/.config/chezmoi/chezmoi.toml` (local)   |
| Behavioral defaults             | `.chezmoidata.yaml`                          | (read by chezmoi, not deployed)            |
| Git identity                    | `dot_config/git/config.tmpl`                 | `~/.config/git/config`                     |
| SSH signing allowlist           | `private_dot_ssh/allowed_signers.tmpl`       | `~/.ssh/allowed_signers`                   |
| 1Password SSH agent keys        | `dot_config/1Password/ssh/agent.toml.tmpl`   | `~/.config/1Password/ssh/agent.toml`       |
| Package manifest                | `dot_Brewfile.tmpl`                          | `~/.Brewfile`                              |
| Terminal config                 | `dot_wezterm.lua.tmpl`                       | `~/.wezterm.lua`                           |
| Shell prompt                    | `dot_config/starship.toml.tmpl`              | `~/.config/starship.toml`                  |
| Environment variables           | `private_dot_env.tmpl`                       | `~/.env` (mode 600)                        |
| Claude Code config              | `dot_claude/`                                | `~/.claude/`                               |
| Documentation                   | `dot_docs/`                                  | `~/.docs/`                                 |
| User scripts                    | `dot_local/bin/`                             | `~/.local/bin/`                            |
