# Setup Guide

Detailed onboarding for new machines and profile changes.

## Before You Begin

This repo is a personal dotfiles template. To use it:
1. **Fork** this repository on GitHub
2. Replace any references to `nehalecky` with your GitHub username
3. Follow the Quick Start steps below with your forked repo URL

## Quick Start

### Option A: Direct config setup (recommended when adapting this repo)

Copy the example config, fill in your values, then apply:

```bash
mkdir -p ~/.config/chezmoi
curl -o ~/.config/chezmoi/chezmoi.toml \
  https://raw.githubusercontent.com/<your-github-username>/dotfiles/master/examples/chezmoi.toml.example
# Edit ~/.config/chezmoi/chezmoi.toml with your values
chezmoi init <your-github-username>   # clones the repo without overwriting your config
chezmoi apply
```

> **Claude Code:** Installed automatically by `chezmoi apply`. If the script
> was skipped or you're setting up without chezmoi, install manually:
> `curl -fsSL https://claude.ai/install.sh | bash`

The example config at `examples/chezmoi.toml.example` documents every field with instructions on where to find the values (especially the 1Password key names, which must match your vault exactly).

### Option B: Interactive guided setup

1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install chezmoi and initialize:
   ```bash
   brew install chezmoi
   chezmoi init --apply <your-github-username>
   ```

3. Answer the setup prompts:
   - **Machine profile**: `personal` or `work`
   - **Git author name**: Your full name
   - **Preferred/casual name**: What you like to be called (defaults to first word of full name)
   - **Git email**: Your email for commits
   - **GitHub username**: Your GitHub handle
   - **Git signing public key**: Your SSH public key (`ssh-ed25519 ...`)
   - **1Password SSH auth key name**: Item name in 1Password for your auth key
   - **1Password signing key name**: Item name in 1Password for your signing key

4. Run brew bundle to install packages:
   ```bash
   brew bundle --global
   ```

5. Claude Code is installed automatically by `chezmoi apply` via the
   `run_once_after_30-install-claude-code.py` script. If it wasn't picked
   up, install manually:
   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

### Re-initializing (change profile or update values)

To change any prompted value, delete it from `~/.config/chezmoi/chezmoi.toml` and re-run:

```bash
chezmoi init --apply <your-github-username>
```

Or edit the value directly in `~/.config/chezmoi/chezmoi.toml` and run `chezmoi apply`.

## What the profiles control

| Setting | `personal` | `work` |
|---------|-----------|--------|
| Git identity | personal email + key | work email + key |
| Brewfile | personal apps (Signal, Spotify, Steam) | work tools (k9s, kubectl, Docker, Slack) |
| Starship prompt | minimal, clean | shows Kubernetes context, hostname |
| SSH allowed_signers | personal key | work key |
| 1Password agent | personal vault keys | work vault keys |
| `.ssh/id_ed25519_signing.pub` | deployed | excluded |
| `.kube/`, `.aws/` | excluded | excluded (managed by cloud CLIs) |

## Day 1 work machine setup (after chezmoi apply)

After running `chezmoi init --apply` with the `work` profile:

1. Authenticate GitHub CLI and verify org access:
   ```bash
   gh auth login
   gh auth status                                                    # confirm logged in
   gh api user/memberships/orgs --jq '.[].organization.login'       # confirm org membership
   ```

2. Set up GCP credentials:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. Authenticate 1Password CLI:
   ```bash
   op signin
   ```

4. **Hand off to your corp onboarding assistant.** Your environment is ready. Open your corporate Claude account and say: *"I just ran chezmoi init on a new work machine — what's next?"* It has access to internal docs, team tooling, and project context to guide the rest of setup.

## Understanding the HOME→Source Workflow

All dotfile changes follow a consistent workflow:

1. **Edit** the actual file in your HOME directory (`~/.zshrc`, `~/.config/starship.toml`, etc.)
2. **Test** that the changes work correctly (reload shell, test configuration)
3. **Sync** to chezmoi with `chezmoi add <file>`
4. **Commit** changes with `chezmoi git -- commit -m "description"`

**Why this workflow**: Direct editing ensures immediate testing. Chezmoi handles synchronization to the source repository.

**Never edit directly in** `~/.local/share/chezmoi/` — always edit in HOME first.

**Example — editing your shell config:**
```bash
# Edit the actual file in HOME
vim ~/.zshrc

# Test changes work
source ~/.zshrc

# Sync to chezmoi source
chezmoi add ~/.zshrc

# Commit with a descriptive message
chezmoi git -- commit -m "feat: add custom shell aliases"
```

### How Chezmoi Manages Files

Chezmoi manages files with three distinct strategies:

| Strategy | Behavior | Examples |
|----------|----------|----------|
| **Managed** | Updates on every `chezmoi apply` | `.zshrc`, `starship.toml`, git config |
| **Create-only** | Deploys once, never overwrites | `.claude/settings.json` |
| **External** | Clones git repos or archives into HOME | `.zprezto` (via `.chezmoiexternal.yaml`) |

**Managed files** follow the HOME→Source workflow above. Chezmoi overwrites them on every apply.

**Create-only files** (`create_` prefix in source) deploy once, then the application owns them. For example, Claude Code modifies `settings.json` at runtime with permission grants — chezmoi seeds the initial version and steps aside. To force a fresh deploy: `rm ~/.claude/settings.json && chezmoi apply`.

**Externals** live in `.chezmoiexternal.yaml`. Chezmoi clones them on first apply and refreshes them periodically (weekly for zprezto).

### `chezmoi init` vs `chezmoi apply`

| Command | When to use |
|---------|------------|
| `chezmoi apply` | Deploy managed files from source to HOME |
| `chezmoi init` | Regenerate config after a "config file template has changed" warning |

`chezmoi init` re-runs the setup prompts (profile, git identity, 1Password keys) and regenerates `~/.config/chezmoi/chezmoi.toml`. Existing values appear as defaults — press Enter to keep them.

## Tool Verification Checklist

After setup, verify everything works:

### Core System
- [ ] Shell loads without errors (`exec zsh`)
- [ ] Starship prompt displays correctly
- [ ] PATH includes `~/.local/bin`

### Authentication
- [ ] 1Password SSH agent working (`ssh-add -L`)
- [ ] GitHub CLI authenticated (`gh auth status`)
- [ ] Git signing configured (`git config commit.gpgsign` — should be `true`)

### Development Tools
- [ ] Python/uv installed (`uv --version`)
- [ ] Node.js installed (`node --version`)
- [ ] Git configured with name and email (`git config --global user.name`)

### TUI Tools
- [ ] File manager launches (`Ctrl+a f` or `yazi`)
- [ ] Editor launches (`Ctrl+a e` or `hx`)
- [ ] Git client launches (`Ctrl+a g` or `lazygit`)
- [ ] System monitor launches (`Ctrl+a p` or `btop`)

### Workspaces
- [ ] Home workspace launches (`workspace-home`)
- [ ] Development workspace launches (`workspace-dev test`)
- [ ] All panes populate correctly

### Claude Code
- [ ] Claude Code installed via native binary (`~/.local/bin/claude` exists)
- [ ] Claude CLI works (`claude --version`)
- [ ] Binary is on PATH (`which claude` returns `~/.local/bin/claude`)

> **Install:** `curl -fsSL https://claude.ai/install.sh | bash`
> Auto-updates in the background. Versions stored at `~/.local/share/claude/versions/`.
> Docs: [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)

> **Migration note:** If Claude Code was previously installed via npm or Homebrew, `chezmoi apply` will detect this and prompt you to migrate to the native binary.

### Claude Code Plugins
- [ ] Claude CLI available (`claude --version`)
- [ ] Superpowers marketplace registered (`claude plugin marketplace list` shows `superpowers-marketplace`)
- [ ] Core plugins installed (`claude plugin list` includes `superpowers`, `elements-of-style`, `episodic-memory`)
- [ ] No dead marketplace entries in `~/.claude/settings.json`

> **Note:** `chezmoi init --apply` automates marketplace registration and plugin installation when the Claude CLI is present. If you need to set up plugins manually:
> ```bash
> claude plugin marketplace add obra/superpowers-marketplace
> claude plugin install superpowers@superpowers-marketplace --scope user
> claude plugin install elements-of-style@superpowers-marketplace --scope user
> claude plugin install episodic-memory@superpowers-marketplace --scope user
> claude plugin install superpowers-developing-for-claude-code@superpowers-marketplace --scope user
> ```

### Voice Notifications

Hooks speak task completion and input prompts via text-to-speech. The local Kokoro neural TTS backend (~90 MB model) downloads from Hugging Face on first use. Pre-warm it before your first Claude Code session to avoid a silent first notification:

```bash
uv run ~/.claude/hooks/utils/tts/kokoro_tts.py "Kokoro ready"
```

To change the Kokoro voice or use a cloud backend, add to `~/.env`:

```bash
export KOKORO_VOICE=af_heart         # default: warm American female ("Her" aesthetic)
# export KOKORO_VOICE=bf_emma        # British female alternative
# See https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md for all options
export ELEVENLABS_API_KEY=your-key   # ElevenLabs (highest quality, overrides Kokoro)
export OPENAI_API_KEY=your-key       # OpenAI TTS (alternative cloud voice)
```

Full reference: [`~/.docs/claude-hooks.md`](dot_docs/claude-hooks.md).

- [ ] Kokoro TTS pre-warmed (`uv run ~/.claude/hooks/utils/tts/kokoro_tts.py "hello"`)
- [ ] (Optional) Cloud TTS key set in `~/.env` for higher-quality voice

### Chezmoi
- [ ] Status command works (`chezmoi status`)
- [ ] Diff shows no unexpected changes (`chezmoi diff`)
- [ ] Can commit changes (`chezmoi git -- status`)

## Troubleshooting

### Config template changed warning

If you see `chezmoi: warning: config file template has changed, run chezmoi init to regenerate config file`, your config needs regeneration (see [`chezmoi init` vs `chezmoi apply`](#chezmoi-init-vs-chezmoi-apply) above). Either:

- Run `chezmoi init --apply <your-github-username>` to regenerate (you will be prompted for new values)
- Or add the missing key manually to `~/.config/chezmoi/chezmoi.toml` under `[data]`

### 1Password SSH signing errors

If commits fail with `1Password: agent returned an error`, ensure:

1. 1Password desktop app is running and unlocked
2. The SSH agent is enabled in 1Password Settings > Developer > SSH Agent
3. The correct key names are set in `~/.config/chezmoi/chezmoi.toml` (`op_auth_key_name`, `op_signing_key_name`)

Verify the agent is active:
```bash
ssh-add -L              # Should list keys from 1Password
echo $SSH_AUTH_SOCK     # Should point to 1Password socket
```

### Checking what chezmoi will change

```bash
chezmoi diff          # Preview all pending changes
chezmoi apply --dry-run  # Dry-run without writing
chezmoi verify        # Validate all managed files
```

### Leader key not working

**Symptoms**: Pressing `Ctrl+a` followed by shortcut keys does nothing.

**Solutions**:
1. Check if another application captures `Ctrl+a` (System Settings > Keyboard > Shortcuts, or tmux/screen running)
2. Restart your terminal
3. Look for "LEADER" indicator in the status bar when pressing `Ctrl+a`

### Tools not found

**Symptoms**: Commands like `yazi`, `lazygit`, or `hx` return "command not found".

```bash
# Check what's missing
brew bundle check --global

# Install missing packages
brew bundle --global

# Verify PATH includes Homebrew
echo $PATH | grep homebrew
```

### Font or symbol issues

**Symptoms**: Boxes, missing icons, or garbled text in the prompt or TUI tools.

```bash
# Install Nerd Font
brew install --cask font-meslo-lg-nerd-font

# Restart WezTerm, then verify font in config
grep "font.*family" ~/.wezterm.lua
```

### Workspace launch failures

**Symptoms**: `workspace-home` or `workspace-dev` commands fail or hang.

```bash
# Check workspace scripts exist
ls -la ~/.local/bin/workspace-*

# Verify zellij is installed
which zellij && zellij --version

# Test individual tools
yazi       # File manager
hx         # Editor
lazygit    # Git client

# Kill a stale session and relaunch
zellij kill-session home
workspace-home
```

### Git authentication problems

**Symptoms**: Git push/pull asks for credentials or fails with authentication errors.

```bash
gh auth status          # Check GitHub CLI auth state
gh auth login           # Re-authenticate if needed
gh auth setup-git       # Configure git to use GitHub CLI
ssh -T git@github.com   # Test SSH to GitHub
```

### Performance issues

**Slow prompt:**
```bash
starship timings        # Diagnose which modules are slow
vim ~/.config/starship.toml  # Comment out slow modules
```

**High CPU or memory:**
```bash
btop                    # Identify runaway processes
# Exit unused TUI apps with 'q'
```
