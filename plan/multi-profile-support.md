# Spec: Multi-Profile Chezmoi Support

**Status:** Draft (Review Complete)
**Author:** Nico Halecky
**Date:** 2026-02-24
**Version:** 1.2

### Changelog

- **v1.2** (2026-02-24): Applied 15 review findings (4 CRITICAL, 5 HIGH, 6 MEDIUM)
  - CRITICAL: Fixed `google-cloud-sdk` to `cask` (not `brew` formula)
  - CRITICAL: Git config template now preserves all 8 sections from source
  - CRITICAL: Personal signing key set as default for `git_signing_key`
  - CRITICAL: Zero-diff claim replaced with honest expected-diff documentation
  - HIGH: Script paths corrected with `.chezmoiscripts/` prefix
  - HIGH: `agent.toml` snapshot corrected (no `vault` field in actual file)
  - HIGH: Added `.zshrc` gcloud sourcing guard (Section 4.3.2)
  - HIGH: Documented `private_dot_gitconfig` GHE consideration (Section 4.4)
  - HIGH: Added brew bundle error handling fix
  - MEDIUM: Rollback plan changed from stash to feature branch
  - MEDIUM: Added first-init migration tip (pre-seed chezmoi.toml)
  - MEDIUM: Clarified `.chezmoiignore` uses target paths, not source paths
  - MEDIUM: Documented `nico@middledata.ai` drop as intentional
  - MEDIUM: Added `run_once_install-wezterm.sh` cleanup (redundant with Brewfile)
  - MEDIUM: Added Starship implementation entry (Section 6)
  - Implementation order updated to include Phase 0 (feature branch) and all new items
  - File change summary updated: 1 new, 7 renames, 4 modifications, 1 deletion, 1 ignore, 1 deferred
- **v1.1** (2026-02-23): Updated with confirmed 1Password Business + GCP
- **v1.0** (2026-02-23): Initial spec

## 1. Problem Statement

The current chezmoi dotfiles setup is hardcoded to a single personal identity. All
git configuration, SSH keys, 1Password agent references, shell environment, and
Brewfile packages assume a personal machine with personal credentials.

This prevents deploying the same framework to a dedicated work machine where:

- Git commits must use a corporate email and signing key
- SSH connections must offer corporate keys
- 1Password Business is the corporate standard (confirmed); personal account linking required
- GCP is the primary cloud platform (confirmed); credential separation required
- Personal applications (gaming, personal messaging) must not be installed
- Platform engineering tools (k8s, GCP, cloud CLIs) should be present

## 2. Goals

1. **Single source of truth**: One chezmoi repo serves both personal and work machines
2. **Init-time identity injection**: `chezmoi init` prompts for profile and identity
3. **Zero personal data on work machines**: No personal email, keys, or apps deployed
4. **Profile-aware Brewfile**: Packages scoped to `all`, `personal`, `work`, and `optional`
5. **No branch divergence**: Profiles handled via templates, not branches
6. **Backward compatible**: Existing personal machine continues working unchanged

## 3. Architecture

### 3.1 Data Flow

```
chezmoi init
    |
    v
.chezmoi.toml.tmpl          # Prompts for profile, identity, key names
    |
    v
~/.config/chezmoi/chezmoi.toml   # LOCAL ONLY, never committed
    |
    v
chezmoi apply
    |
    +-- .chezmoidata.yaml         # Static defaults (committed)
    +-- chezmoi.toml [data]       # Machine-specific overrides (local)
    +-- .chezmoi.* built-ins      # OS, hostname, username (auto)
    |
    v
Merged template data (.profile, .git_email, .isWork, etc.)
    |
    +-- *.tmpl files              # Render with merged data
    +-- .chezmoiignore            # Exclude files by profile
    +-- run_onchange_* scripts    # Install profile-scoped packages
```

### 3.2 Key Design Decisions


| Decision                | Choice                                                 | Rationale                                          |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------- |
| Profile mechanism       | `promptChoiceOnce` in `.chezmoi.toml.tmpl`             | Prompts once at init, persists locally             |
| Brewfile approach       | `dot_Brewfile.tmpl` (templated file)                   | Preserves existing `brew bundle --global` workflow |
| Package install trigger | `run_onchange_` with Brewfile content hash             | Re-runs only when rendered Brewfile changes        |
| Wezterm paths           | Fix in Lua (`os.getenv('HOME')`)                       | Avoids Go template / Lua `{{` delimiter conflict   |
| 1Password accounts      | Linked personal + Business accounts                    | Descript uses 1Password Business (confirmed)       |
| Secret injection        | `onepasswordRead` with profile-conditional vault paths | Future enhancement, not in initial scope           |
| Cloud platform          | GCP primary; gcloud config separation                  | Descript uses GCP (confirmed)                      |
| Claude config.json      | Exclude from chezmoi                                   | Runtime state that conflicts across accounts       |


### 3.3 Template Variable Schema

Variables provided by `.chezmoi.toml.tmpl` prompts (stored in local `chezmoi.toml`):

```yaml
# Identity
profile: "personal" | "work"       # Machine profile
git_name: "Nicholaus Halecky"       # Git commit author name
git_email: "user@example.com"       # Git commit author email
github_username: "nehalecky"        # GitHub username

# SSH & Signing
git_signing_key: "ssh-ed25519 AAAA..."  # Public key for commit signing
op_auth_key_name: "GitHub Auth Key"     # 1Password item name for SSH auth
op_signing_key_name: "Signing Key"      # 1Password item name for signing

# Derived (computed in template, not prompted)
isWork: true/false                  # profile == "work"
isPersonal: true/false              # profile == "personal"
```

Variables retained in `.chezmoidata.yaml` (static defaults, committed):

```yaml
# Unchanged - these are behavioral, not identity
starship:
  profile: "personal"  # NOTE: will be overridden by .profile on work machines
  show_kubernetes: false
  ...
```

## 4. File Changes

### 4.1 New Files to Create

#### `.chezmoi.toml.tmpl` - Init-Time Prompts

**Location:** `~/.local/share/chezmoi/.chezmoi.toml.tmpl`

```toml
{{- /* ── Profile Selection ─────────────────────────────────── */ -}}
{{- $profiles := list "personal" "work" -}}
{{- $profile := promptChoiceOnce . "profile" "Machine profile" $profiles "personal" -}}

{{- /* ── Identity ──────────────────────────────────────────── */ -}}
{{- $git_name := promptStringOnce . "git_name" "Git author name" "Nicholaus Halecky" -}}
{{- $git_email := "" -}}
{{- $github_username := "" -}}
{{- if eq $profile "personal" -}}
{{-   $git_email = promptStringOnce . "git_email" "Git email" "nehalecky@gmail.com" -}}
{{-   $github_username = promptStringOnce . "github_username" "GitHub username" "nehalecky" -}}
{{- else -}}
{{-   $git_email = promptStringOnce . "git_email" "Work git email" "" -}}
{{-   $github_username = promptStringOnce . "github_username" "Work GitHub username" "" -}}
{{- end -}}

{{- /* ── SSH & Signing ─────────────────────────────────────── */ -}}
{{- $git_signing_key := "" -}}
{{- $op_auth_key_name := "" -}}
{{- $op_signing_key_name := "" -}}
{{- if eq $profile "personal" -}}
{{-   $git_signing_key = promptStringOnce . "git_signing_key" "Git signing public key" "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGfxtbZHZuHkiMv2ZXR52KSwROrTXK0wyxoX8yd88Ih6" -}}
{{-   $op_auth_key_name = promptStringOnce . "op_auth_key_name" "1Password SSH auth key name" "Nico Personal GitHub Auth Key" -}}
{{-   $op_signing_key_name = promptStringOnce . "op_signing_key_name" "1Password signing key name" "Github Signing Key (Nico Personal)" -}}
{{- else -}}
{{-   $git_signing_key = promptStringOnce . "git_signing_key" "Work git signing public key (ssh-ed25519 ...)" "" -}}
{{-   $op_auth_key_name = promptStringOnce . "op_auth_key_name" "1Password SSH auth key name" "GitHub Auth Key" -}}
{{-   $op_signing_key_name = promptStringOnce . "op_signing_key_name" "1Password signing key name" "Signing Key" -}}
{{- end -}}

[data]
    profile             = {{ $profile | quote }}
    isWork              = {{ eq $profile "work" }}
    isPersonal          = {{ eq $profile "personal" }}
    git_name            = {{ $git_name | quote }}
    git_email           = {{ $git_email | quote }}
    github_username     = {{ $github_username | quote }}
    git_signing_key     = {{ $git_signing_key | quote }}
    op_auth_key_name    = {{ $op_auth_key_name | quote }}
    op_signing_key_name = {{ $op_signing_key_name | quote }}
```

**Behavior:**

- On a fresh machine: prompts for every value
- On re-init: reads existing values silently (the `Once` suffix)
- To re-prompt: delete the key from `~/.config/chezmoi/chezmoi.toml`

**First init on existing personal machine:** Since no `~/.config/chezmoi/chezmoi.toml`
exists yet, `chezmoi init` will prompt for ALL values even on the personal machine.
The defaults are pre-filled with the current personal values, so the user can press
Enter for each prompt to accept them. After this one-time setup, subsequent
`chezmoi init` calls will be silent.

**Migration tip:** To pre-seed the config and skip prompts entirely, create
`~/.config/chezmoi/chezmoi.toml` manually before running `chezmoi init`:

```bash
# Optional: pre-seed to avoid prompts on personal machine
mkdir -p ~/.config/chezmoi
cat > ~/.config/chezmoi/chezmoi.toml << 'EOF'
[data]
    profile = "personal"
    isWork = false
    isPersonal = true
    git_name = "Nicholaus Halecky"
    git_email = "nehalecky@gmail.com"
    github_username = "nehalecky"
    git_signing_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGfxtbZHZuHkiMv2ZXR52KSwROrTXK0wyxoX8yd88Ih6"
    op_auth_key_name = "Nico Personal GitHub Auth Key"
    op_signing_key_name = "Github Signing Key (Nico Personal)"
EOF
```

---

### 4.2 Files to Convert to Templates

Each file below gets renamed from `<name>` to `<name>.tmpl` in the chezmoi source.

#### 4.2.1 `dot_config/git/config` -> `dot_config/git/config.tmpl`

**Current (hardcoded — all 8 sections):**

```gitconfig
# Git Configuration
# Managed by chezmoi

[user]
    name = Nicholaus Halecky
    email = nehalecky@gmail.com

[commit]
    gpgsign = true

[gpg]
    format = ssh

[gpg "ssh"]
    allowedSignersFile = /Users/nehalecky/.ssh/allowed_signers
    program = "/Applications/1Password.app/Contents/MacOS/op-ssh-sign"

[user]
    signingkey = ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGfxtbZHZuHkiMv2ZXR52KSwROrTXK0wyxoX8yd88Ih6

[init]
    defaultBranch = main

[pull]
    rebase = false

[core]
    editor = code --wait
```

**Target (templated — preserving all 8 sections):**

```gitconfig
# Git Configuration
# Managed by chezmoi

[user]
    name = {{ .git_name }}
    email = {{ .git_email }}

[commit]
    gpgsign = true

[gpg]
    format = ssh

[gpg "ssh"]
    allowedSignersFile = {{ .chezmoi.homeDir }}/.ssh/allowed_signers
    program = "/Applications/1Password.app/Contents/MacOS/op-ssh-sign"

{{- if .git_signing_key }}
[user]
    signingkey = {{ .git_signing_key }}
{{- end }}

[init]
    defaultBranch = main

[pull]
    rebase = false

[core]
    editor = code --wait
```

**What changes:** 4 hardcoded values become template variables (`name`, `email`,
`allowedSignersFile` path prefix, `signingkey`). All 8 sections from the current
file are preserved. The `[commit]`, `[gpg]`, `[gpg "ssh"] program`, `[init]`,
`[pull]`, and `[core]` sections are identical to current — no regressions.

---

#### 4.2.2 `private_dot_ssh/allowed_signers` -> `private_dot_ssh/allowed_signers.tmpl`

**Current:**

```
nehalecky@gmail.com ssh-ed25519 AAAA...
nico@middledata.ai ssh-ed25519 AAAA...
```

**Target:**

```
{{ .git_email }} {{ .git_signing_key }}
```

**What changes:** Single entry using the active profile's email and signing key.
Only the current profile's identity is present. No stale personal entries on work
machines.

**Known regression on personal machine:** The current file has TWO entries
(`nehalecky@gmail.com` and `nico@middledata.ai`), both using the same public key.
The template produces only ONE entry. This is an **intentional simplification** —
the `nico@middledata.ai` identity is from a prior business (middledata.ai) that
is no longer active. Dropping it is acceptable.

**If you need to verify old commits signed under a different email,** add entries
manually to `~/.ssh/allowed_signers` after deployment. Chezmoi will not overwrite
manual additions unless `chezmoi apply` is run again (at which point the template
re-renders the file).

---

#### 4.2.3 `dot_config/1Password/ssh/agent.toml` -> `dot_config/1Password/ssh/agent.toml.tmpl`

**Current (actual file — no `vault` field):**

```toml
# 1Password SSH Agent Configuration
# This controls which SSH keys the agent offers to SSH servers

# Only offer the GitHub authentication key first
[[ssh-keys]]
item = "Nico Personal GitHub Auth Key"

# Then offer the signing key for other purposes
[[ssh-keys]]
item = "Github Signing Key (Nico Personal)"
```

**Target:**

```toml
[[ssh-keys]]
item = {{ .op_auth_key_name | quote }}

[[ssh-keys]]
item = {{ .op_signing_key_name | quote }}
```

**What changes:** Item names become variables. Vault field removed (1Password
resolves items across linked accounts automatically when personal and Business
accounts are linked). Descript uses 1Password Business (confirmed), so the work
machine will have the Business account as primary with items in a work vault.
The `op_auth_key_name` and `op_signing_key_name` prompts at init time set the
correct item names per profile.

---

#### 4.2.4 `private_dot_ssh/id_ed25519_signing.pub` - Conditional Inclusion

This file contains the personal signing public key. Rather than templating it,
**exclude it on work machines** via `.chezmoiignore`:

```
{{ if .isWork }}
.ssh/id_ed25519_signing.pub
{{ end }}
```

The work machine's signing key lives in 1Password and is offered by the agent.
No static public key file is needed.

---

#### 4.2.5 `dot_claude/memories/personal/user-info.md` -> `dot_claude/memories/personal/user-info.md.tmpl`

**Current:**

```markdown
- **Full Name**: Nicholaus Eugene Halecky
- **Preferred Name**: Nico
- **GitHub Username**: nehalecky
```

**Target:**

```markdown
- **Full Name**: {{ .git_name }}
- **Preferred Name**: Nico
- **GitHub Username**: {{ .github_username }}
{{- if .isWork }}
- **Work Profile**: Active
- **Work Email**: {{ .git_email }}
{{- end }}
```

---

#### 4.2.6 `dot_Brewfile` -> `dot_Brewfile.tmpl`

See Section 5 (Brewfile Profile Configuration) for full specification.

---

### 4.3 Files to Modify (No Template Conversion)

#### 4.3.1 `dot_wezterm.lua` - Fix Hardcoded Paths

The file has two hardcoded `/Users/nehalecky/` paths but is otherwise clean.
Because Lua uses `{{` for table literals, converting to a `.tmpl` would require
escaping throughout the file. Instead, fix the two paths in Lua natively.

**Lines to change:**

```lua
-- BEFORE (line ~281):
args = { '/Users/nehalecky/.local/bin/workspace-home' },
-- AFTER:
args = { wezterm.home_dir .. '/.local/bin/workspace-home' },

-- BEFORE (line ~290):
args = { '/Users/nehalecky/.local/bin/workspace-dev' },
-- AFTER:
args = { wezterm.home_dir .. '/.local/bin/workspace-dev' },
```

**Rationale:** `wezterm.home_dir` is already used elsewhere in the file (line 309).
This is the idiomatic WezTerm approach and avoids template engine conflicts.

---

#### 4.3.2 `dot_zshrc` - Guard gcloud SDK Sourcing

Lines 154-155 unconditionally source Google Cloud SDK shell integration:

```bash
# Current (fails if gcloud not installed):
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
source /opt/homebrew/share/google-cloud-sdk/completion.zsh.inc
```

Since `google-cloud-sdk` is only in the work Brewfile, these lines would break on
a personal machine that removes it (or on first apply before brew bundle runs).
Add an existence guard:

```bash
# AFTER:
if [[ -f /opt/homebrew/share/google-cloud-sdk/path.zsh.inc ]]; then
  source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
  source /opt/homebrew/share/google-cloud-sdk/completion.zsh.inc
fi
```

**Note:** This is a Lua-style fix — edit the file directly, no `.tmpl` needed.
The guard makes it safe regardless of whether gcloud is installed. Added to Phase 4.

---

#### 4.3.3 `.chezmoidata.yaml` - Remove Identity, Keep Behavior

**Remove:** The `is_work` key (now provided by `.chezmoi.toml.tmpl`).
**Remove:** The `system.`* block (now uses chezmoi built-ins directly).
**Keep:** All `starship.`* settings.

The `starship.profile` default should remain `"personal"` -- on work machines, the
profile override from `chezmoi.toml` takes precedence (chezmoi.toml data wins
over .chezmoidata.yaml in the merge order).

**Updated file:**

```yaml
# Chezmoi data for machine-specific configurations
# Identity data is provided by .chezmoi.toml.tmpl at init time.
# This file contains behavioral defaults only.

# Starship prompt configuration
starship:
  show_time: true
  show_kubernetes: false
  git_truncation: 20
  dir_truncation: 3
  prompt_theme: "p10k"
```

---

#### 4.3.4 `.chezmoiignore` - Add Profile-Conditional Exclusions

**Append to existing file.**

**Path format note:** `.chezmoiignore` uses **target paths** (as they appear in
the home directory), not source paths. So `.ssh/id_ed25519_signing.pub` is
correct, not `private_dot_ssh/id_ed25519_signing.pub`.

```
# Profile-conditional exclusions

# Personal signing key not needed on work machines
{{ if .isWork }}
.ssh/id_ed25519_signing.pub
{{ end }}

# Work-specific configs not on personal machines
{{ if .isPersonal }}
.kube/
.aws/
{{ end }}

# Claude runtime config (runtime state, conflicts across accounts)
.config/claude/config.json
```

**Important:** The last line uses `.config/claude/config.json` (target path),
not `dot_config/claude/config.json` (source path). The `.chezmoiignore` file
always uses target paths.

---

#### 4.3.5 `.chezmoiscripts/run_once_after_20-brew-bundle.sh` -> `.chezmoiscripts/run_onchange_after_20-brew-bundle.sh.tmpl`

**Rename** the existing brew bundle script to:

- Change `run_once_` to `run_onchange_` (re-run when Brewfile changes)
- Add `.tmpl` extension (to inject Brewfile content hash for change detection)

**Add this line near the top of the script (after the shebang):**

```bash
# Brewfile hash: {{ include "dot_Brewfile.tmpl" | sha256sum }}
```

This ensures the script re-executes whenever the rendered Brewfile content changes
(e.g., when a package is added or the profile changes).

**Error handling fix:** The existing script uses `set -eufo pipefail`, which causes
the entire script to abort if a single cask fails to install (common with
quarantine prompts, download timeouts, or cask signing issues). Change the
`brew bundle` invocation to tolerate partial failures:

```bash
# Replace the existing brew bundle line:
brew bundle --no-lock || {
  echo "⚠️  Some packages failed to install. Run 'brew bundle --no-lock' manually to retry."
}
```

Alternatively, remove the `-e` flag from the `set` line for this script. Either
approach prevents a single cask failure from blocking all subsequent verification.

The rest of the script body remains unchanged -- it already reads `$HOME/.Brewfile`
via `brew bundle --no-lock`.

---

### 4.4 Files Requiring Attention (Not Templated in v1)

#### 4.4.1 `private_dot_gitconfig` - Credential Helper for GitHub

This file redirects to `~/.config/git/config` and configures `gh` as the
credential helper for `github.com` and `gist.github.com`:

```gitconfig
[include]
    path = ~/.config/git/config
[credential "https://github.com"]
    helper =
    helper = !/opt/homebrew/bin/gh auth git-credential
[credential "https://gist.github.com"]
    helper =
    helper = !/opt/homebrew/bin/gh auth git-credential
```

**v1 action:** No template conversion needed. The credential helper for
`github.com` works for both personal and work profiles (GitHub, not GHE).

**If Descript uses GitHub Enterprise (GHE):** A future v2 enhancement would
convert this to `private_dot_gitconfig.tmpl` and add a conditional credential
block:

```gitconfig
{{ if .isWork -}}
[credential "https://github.descript.com"]
    helper =
    helper = !/opt/homebrew/bin/gh auth git-credential
{{ end -}}
```

**Confirm during onboarding:** Does Descript use GitHub.com or a GHE instance?
If GHE, note the domain for a v2 update.

---

### 4.5 Files to Clean Up

#### 4.5.0 `.chezmoiscripts/run_once_install-wezterm.sh` - Redundant with Brewfile

This script does `brew install --cask wezterm`, which is already handled by
`cask "wezterm"` in the Brewfile. With the `run_onchange_` brew bundle script
running on every Brewfile change, this standalone script is redundant.

**Action:** Delete this script. WezTerm installation is covered by the Brewfile.

---

### 4.6 Files to Remove from Chezmoi Management

#### 4.6.1 `dot_config/claude/config.json`

This file contains OAuth tokens, user IDs, and session history that are
account-specific runtime state. It should not be deployed across machines.

**Action:** Add `dot_config/claude/config.json` to `.chezmoiignore` and run
`chezmoi forget ~/.config/claude/config.json`.

---

## 5. Brewfile Profile Configuration

### 5.1 Profile Categories

Every package is assigned to one of four profiles:


| Profile    | Meaning                               | Deployed When                 |
| ---------- | ------------------------------------- | ----------------------------- |
| `all`      | Universal development toolchain       | Always                        |
| `work`     | Platform engineering & corporate apps | `profile == "work"`           |
| `personal` | Gaming, personal messaging, hobbies   | `profile == "personal"`       |
| `optional` | User preference, either profile       | Controlled by a separate flag |


### 5.2 Package Assignment

#### Taps (all profiles)

```ruby
tap "romkatv/powerlevel10k"
```

#### Brew - All Profiles

```ruby
# Core development
brew "bash"
brew "bat"
brew "chezmoi"
brew "delta"
brew "eza"
brew "fd"
brew "fzf"
brew "gh"
brew "git"
brew "glow"
brew "jq"
brew "just"
brew "lazygit"
brew "node"
brew "ripgrep"
brew "tealdeer"
brew "uv"
brew "wget"

# Shell & terminal
brew "starship"
brew "yazi"
brew "zellij"
brew "zsh"

# Editors
brew "helix"
brew "marksman"

# System utilities
brew "btop"
brew "dust"
brew "procs"

# AI & ML tools
brew "fabric-ai"
brew "llm"

# Containers & infra
brew "lazydocker"

# Productivity
brew "task"
brew "taskwarrior-tui"

# API & networking
brew "atac"
brew "bandwhich"
```

#### Brew - Work Only

```ruby
# Platform engineering - core (confirmed Descript stack)
brew "cosign"
brew "k9s"
brew "kubectl"
brew "helm"
brew "kustomize"
cask "google-cloud-sdk"      # GCP CLI (confirmed primary cloud)
                              # NOTE: This is a Homebrew cask, not a formula.
                              # `brew info google-cloud-sdk` resolves to cask "gcloud-cli".

# Platform engineering - likely (confirm during onboarding)
# brew "terraform"
# brew "temporal"             # Workflow orchestration (seen in job postings)
# brew "argocd"               # GitOps (common with k8s + GCP)
```

#### Brew - Optional (either profile, user preference)

```ruby
brew "corelocationcli"
brew "emacs"
brew "speedtest-cli"
```

#### Cask - All Profiles

```ruby
cask "1password"
cask "1password-cli"
cask "claude"
cask "claude-code"
cask "font-awesome-terminal-fonts"
cask "font-meslo-lg-nerd-font"
cask "obsidian"
cask "raycast"
cask "visual-studio-code"
cask "wezterm"
```

#### Cask - Work Only

```ruby
cask "slack"
cask "zoom"
cask "docker"                 # Container runtime (confirmed in job postings)
# NOTE: Extend as needed:
# cask "notion"               # Knowledge management (confirmed via case study)
# cask "linear"               # Issue tracking (has Descript integration)
```

#### Cask - Personal Only

```ruby
cask "pokemon-tcg-live"
cask "signal"
cask "sonic-pi"
cask "spotify"
cask "steam"
cask "telegram"
cask "whatsapp"
```

#### Cask - Optional (included in both profiles by default)

```ruby
cask "arc"
cask "cursor"
cask "firefox"
cask "github"
cask "protonvpn"
cask "vlc"
cask "zotero"
```

#### VS Code Extensions - All Profiles

```ruby
vscode "davidanson.vscode-markdownlint"
vscode "github.copilot"
vscode "github.copilot-chat"
vscode "ms-python.debugpy"
vscode "ms-python.python"
vscode "ms-python.vscode-pylance"
vscode "ms-toolsai.jupyter"
vscode "ms-toolsai.jupyter-keymap"
vscode "ms-toolsai.jupyter-renderers"
vscode "ms-toolsai.vscode-jupyter-cell-tags"
vscode "shd101wyy.markdown-preview-enhanced"
vscode "yzhang.markdown-all-in-one"
```

#### VS Code Extensions - Optional

```ruby
vscode "ms-toolsai.vscode-jupyter-slideshow"
```

### 5.3 Template Structure

The `dot_Brewfile.tmpl` uses Go template conditionals to include/exclude sections:

```ruby
# Managed by chezmoi - do not edit directly
# Profile: {{ .profile }}
# Generated: {{ now | date "2006-01-02" }}

tap "romkatv/powerlevel10k"

# ── Core Development ────────────────────────────────────────
brew "bash"
brew "bat"
# ... (all "all" profile brew packages listed in 5.2)

# ── Cask - All Profiles ────────────────────────────────────
cask "1password"
cask "1password-cli"
# ... (all "all" profile cask packages listed in 5.2)

{{ if .isWork -}}
# ── Platform Engineering (work only) ────────────────────────
brew "cosign"
brew "k9s"
brew "kubectl"
brew "helm"
brew "kustomize"
cask "google-cloud-sdk"
{{ end -}}

{{ if .isWork -}}
# ── Work Applications ───────────────────────────────────────
cask "docker"
cask "slack"
cask "zoom"
{{ end -}}

{{ if .isPersonal -}}
# ── Personal Applications ───────────────────────────────────
cask "pokemon-tcg-live"
cask "signal"
cask "sonic-pi"
cask "spotify"
cask "steam"
cask "telegram"
cask "whatsapp"
{{ end -}}

# ── Optional (both profiles) ───────────────────────────────
brew "corelocationcli"
brew "emacs"
brew "speedtest-cli"
cask "arc"
cask "cursor"
cask "firefox"
cask "github"
cask "protonvpn"
cask "vlc"
cask "zotero"

# ── VS Code Extensions ─────────────────────────────────────
vscode "davidanson.vscode-markdownlint"
# ... (all extensions listed in 5.2)
```

### 5.4 Confirmed Descript Stack

The following are confirmed and included in the work-only Brewfile sections above:

- **GCP** (confirmed primary cloud) -- `cask "google-cloud-sdk"` in work Brewfile (resolves to `gcloud-cli` cask)
- **Kubernetes** (confirmed) -- `kubectl`, `helm`, `kustomize`, `k9s`
- **Docker** (confirmed) -- `docker` cask in work Brewfile
- **1Password Business** (confirmed) -- `1password` + `1password-cli` already in `all`

Still to confirm during onboarding week:

- **Temporal** -- workflow orchestration (seen in job postings)
- **Notion** -- knowledge management (confirmed via case study, but may be web-only)
- **Linear** -- issue tracking (has Descript integration)
- **Terraform/Pulumi** -- IaC tool choice

**GCP credential note:** Google Cloud SDK is sourced in `.zshrc` via Homebrew
on the personal machine. On the work machine, the work Brewfile installs it
fresh. GCP credential separation via `gcloud config configurations` is a
runtime operation handled during onboarding (see Section 7.1).

## 6. Starship Prompt Integration

The starship configuration already has `personal.toml` and `work.toml` themes.
Wire the profile to the theme selection.

### 6.1 Implementation

The existing `dot_config/starship.toml` should become `dot_config/starship.toml.tmpl`
that references `.profile` directly:

```toml
# Starship Configuration
# Profile: {{ .profile }}
# Managed by chezmoi

{{ if eq .profile "personal" -}}
# Personal theme - minimal, clean
source = "~/.config/starship/themes/personal.toml"
{{ else -}}
# Work theme - shows kubernetes context, hostname
source = "~/.config/starship/themes/work.toml"
{{ end -}}
```

**Alternatively**, if the current `starship.toml` already uses `starship.profile`
from `.chezmoidata.yaml`, simply replace those references with `.profile` (from
`chezmoi.toml`). The `.chezmoidata.yaml` `starship.profile` field is then
redundant and can be removed (it was already slated for removal in Section 4.3.3).

The `work.toml` theme already shows kubernetes context and hostname -- appropriate
for a platform engineering role.

### 6.2 Implementation Phase

Added to **Phase 2** (Identity Templates) since it's a simple template conversion
with no dependencies beyond the `.chezmoi.toml.tmpl` foundation from Phase 1.

## 7. Future Enhancements (Out of Initial Scope)

These are documented for awareness but not implemented in v1:

### 7.1 GCP Credential Separation (Confirmed: Descript uses GCP)

Descript's infrastructure runs on GCP. The work machine needs isolated gcloud
credentials that don't cross-contaminate with any personal GCP projects.

**Day 1 runtime setup:**

```bash
# Create a named gcloud configuration for Descript
gcloud config configurations create descript
gcloud config configurations activate descript
gcloud auth login
gcloud config set project <descript-project-id>

# Application default credentials for SDK/terraform
gcloud auth application-default login
```

**Optional dotfiles enhancement (Phase 2):**
Add a `CLOUDSDK_ACTIVE_CONFIG_NAME` export to the shell environment, conditional
on profile, to ensure the correct gcloud config is always active:

```bash
# In dot_zshenv.tmpl (future):
{{ if .isWork -}}
export CLOUDSDK_ACTIVE_CONFIG_NAME="descript"
{{ end -}}
```

This is a runtime operation for v1. The dotfiles enhancement is deferred.

### 7.2 1Password Secret Injection via Templates (Confirmed: Descript uses 1Password)

Descript uses 1Password Business. On the work machine, the Business account will
be primary. Personal account can be linked for cross-vault access if desired.

Replace `.env.tmpl` placeholder comments with real `onepasswordRead` calls:

```bash
{{ if .isWork -}}
export GCP_SERVICE_ACCOUNT_KEY={{ onepasswordRead "op://Descript/gcp-sa/key" }}
{{ end -}}

{{ if .isPersonal -}}
export OPENAI_API_KEY={{ onepasswordRead "op://Personal/openai/api_key" }}
{{ end -}}
```

The `op://` vault path prefix maps to the 1Password vault name. On the work
machine, the Descript vault is available via the Business account. On the personal
machine, the Personal vault is available via the individual account.

Defer implementation until the work 1Password account is provisioned and vault
structure is known.

### 7.3 Kubernetes Config Management

```
# .chezmoiignore - future
{{ if .isPersonal }}
.kube/
{{ end }}
```

Kubernetes config (`~/.kube/config`) is typically managed by cloud CLIs
(`gcloud container clusters get-credentials`, `aws eks update-kubeconfig`), not
by dotfiles. The `.chezmoiignore` entry prevents chezmoi from interfering.

### 7.4 Conditional Claude Code Agent Ecosystem

Some agents (e.g., `google-workspace.md`, `executive-assistant.md`) reference
personal services. Consider per-profile agent variants or conditional content
in agent files. Low priority -- agents work fine as-is on work machines.

## 8. Implementation Order

Tasks should be implemented in this order due to dependencies:

```
Phase 0: Setup
  0.1  Create feature branch: chezmoi git -- checkout -b feat/multi-profile-support
  0.2  Optional: pre-seed ~/.config/chezmoi/chezmoi.toml on personal machine

Phase 1: Foundation
  1.1  Create .chezmoi.toml.tmpl (init prompts with profile-conditional defaults)
  1.2  Update .chezmoidata.yaml (remove identity + system blocks, keep starship behavior)
  1.3  Update .chezmoiignore (profile conditionals + claude config, using target paths)

Phase 2: Identity Templates
  2.1  Convert dot_config/git/config -> .tmpl (ALL 8 sections preserved)
  2.2  Convert private_dot_ssh/allowed_signers -> .tmpl (single-entry, intentional)
  2.3  Convert dot_config/1Password/ssh/agent.toml -> .tmpl (no vault field)
  2.4  Convert dot_claude/memories/personal/user-info.md -> .tmpl
  2.5  Convert dot_config/starship.toml -> .tmpl (wire .profile to theme)

Phase 3: Brewfile
  3.1  Convert dot_Brewfile -> dot_Brewfile.tmpl with profile sections
       (google-cloud-sdk as cask, not brew formula)
  3.2  Rename .chezmoiscripts/run_once_after_20-brew-bundle.sh ->
       .chezmoiscripts/run_onchange_after_20-brew-bundle.sh.tmpl
       (add hash line + fix error handling for brew bundle)
  3.3  Delete .chezmoiscripts/run_once_install-wezterm.sh (redundant with Brewfile)

Phase 4: Path & Shell Fixes
  4.1  Fix dot_wezterm.lua hardcoded paths (Lua-native, no template)
  4.2  Guard gcloud SDK sourcing in dot_zshrc (existence check)
  4.3  Fix dot_config/iterm2 hardcoded path (template or ignore)

Phase 5: Verification
  5.1  Run chezmoi diff on personal machine — expect only known diffs
       (see Section 9.1 for expected diff list)
  5.2  Test chezmoi init --apply in a temp directory with work profile
  5.3  Verify Brewfile renders correctly for both profiles
  5.4  Verify git config, SSH config, 1Password config render correctly
  5.5  Merge feature branch to master after verification
```

## 9. Verification Plan

### 9.1 Personal Machine (Regression)

After all changes, running `chezmoi diff` on the current personal machine should
show a **minimal, well-understood diff**. Most defaults in `.chezmoi.toml.tmpl`
match the current hardcoded values, but these known differences are expected:

**Expected diffs on personal machine (accept all defaults):**

1. `~/.ssh/allowed_signers` — Drops the `nico@middledata.ai` second line (by design:
  template produces single-entry file using active profile identity)
2. `~/.config/1Password/ssh/agent.toml` — Comments removed (template output is
  clean, without the original inline comments)
3. `~/.Brewfile` — Gains a header comment (`# Profile: personal`, date), and
  optional packages may be reordered

**No diff expected for:**

- `~/.config/git/config` — all 8 sections preserved with matching defaults
- `~/.wezterm.lua` — Lua-native path fix produces functionally identical output
- `~/.claude/memories/personal/user-info.md` — template defaults match current content

**Test command:**

```bash
chezmoi init --apply  # should prompt, accept defaults
chezmoi diff          # review diff — should only show expected items above
```

**Acceptance criteria:** No *unintended* diffs. The known diffs above are
acceptable and intentional (removing stale middledata.ai identity, normalizing
comments).

### 9.2 Work Profile (New Machine Simulation)

```bash
# Create a temporary chezmoi config with work profile
chezmoi execute-template --init \
  --promptChoice "profile=work" \
  --promptString "git_name=Nico Halecky" \
  --promptString "git_email=nhalecky@descript.com" \
  --promptString "github_username=nhalecky-descript" \
  --promptString "git_signing_key=ssh-ed25519 TESTKEY123" \
  --promptString "op_auth_key_name=Descript GitHub Auth Key" \
  --promptString "op_signing_key_name=Descript Signing Key" \
  < .chezmoi.toml.tmpl
```

**Verify rendered files:**

```bash
chezmoi cat ~/.config/git/config   # should show descript email
chezmoi cat ~/.Brewfile            # should have slack/zoom, no steam/spotify
chezmoi cat ~/.ssh/allowed_signers # should show descript email + key
chezmoi ignored                    # should include .ssh/id_ed25519_signing.pub
```

### 9.3 Brewfile Content Verification

```bash
# Render Brewfile for work profile and check
chezmoi cat ~/.Brewfile | grep -c "steam"     # should be 0
chezmoi cat ~/.Brewfile | grep -c "slack"     # should be 1
chezmoi cat ~/.Brewfile | grep -c "k9s"       # should be 1
chezmoi cat ~/.Brewfile | grep -c "spotify"   # should be 0

# Render Brewfile for personal profile and check
chezmoi cat ~/.Brewfile | grep -c "steam"     # should be 1
chezmoi cat ~/.Brewfile | grep -c "slack"     # should be 0
```

## 10. Rollback Plan

Implementation MUST happen on a feature branch to protect the working `master`:

1. **Before any changes:** `chezmoi git -- checkout -b feat/multi-profile-support`
2. **During implementation:** Each phase is a separate commit on the feature branch
3. **If personal machine breaks:** `chezmoi git -- checkout master && chezmoi apply`
  restores the known-good state immediately
4. **If feature branch is salvageable:** Fix on the branch, commit, retry
5. **If feature branch is unsalvageable:** `chezmoi git -- branch -D feat/multi-profile-support`
  and start over — master is untouched
6. **When verified:** `chezmoi git -- checkout master && chezmoi git -- merge feat/multi-profile-support`

## 11. File Change Summary


| Action | File (chezmoi source path)                                                               | Description                                         |
| ------ | ---------------------------------------------------------------------------------------- | --------------------------------------------------- |
| CREATE | `.chezmoi.toml.tmpl`                                                                     | Init-time prompts for profile + identity            |
| RENAME | `dot_config/git/config` -> `.tmpl`                                                       | Template git identity + signing (all 8 sections)    |
| RENAME | `private_dot_ssh/allowed_signers` -> `.tmpl`                                             | Template signing identity (single entry)            |
| RENAME | `dot_config/1Password/ssh/agent.toml` -> `.tmpl`                                         | Template key item names (no vault field)            |
| RENAME | `dot_claude/memories/personal/user-info.md` -> `.tmpl`                                   | Template user identity                              |
| RENAME | `dot_Brewfile` -> `.tmpl`                                                                | Profile-conditional packages (gcloud as cask)       |
| RENAME | `.chezmoiscripts/run_once_after_20...` -> `.chezmoiscripts/run_onchange_after_20...tmpl` | Change detection + hash + error handling            |
| RENAME | `dot_config/starship.toml` -> `.tmpl`                                                    | Wire `.profile` to theme selection                  |
| MODIFY | `.chezmoidata.yaml`                                                                      | Remove identity + system blocks, keep starship      |
| MODIFY | `.chezmoiignore`                                                                         | Profile conditionals + claude config (target paths) |
| MODIFY | `dot_wezterm.lua`                                                                        | Fix 2 hardcoded paths with `wezterm.home_dir`       |
| MODIFY | `dot_zshrc`                                                                              | Guard gcloud SDK sourcing with existence check      |
| DELETE | `.chezmoiscripts/run_once_install-wezterm.sh`                                            | Redundant with Brewfile cask                        |
| IGNORE | `.config/claude/config.json`                                                             | Add to .chezmoiignore (target path)                 |
| NOTE   | `private_dot_gitconfig`                                                                  | v2: add GHE credential block if needed              |


**Total: 1 new, 7 renames, 4 modifications, 1 deletion, 1 ignore, 1 deferred**