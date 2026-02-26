# Setup Guide

Onboarding for new machines and profile changes.

## Before You Begin

This repo is a personal dotfiles template.
1. **Fork** this repository on GitHub
2. Replace all references to `nehalecky` with your GitHub username
3. Follow the Quick Start steps below with your forked repo URL

## Quick Start

### New machine setup

1. Install Homebrew (skip if already installed):
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
   - **Preferred/casual name**: How you prefer to be addressed (defaults to first word of full name)
   - **Git email**: Your email for commits
   - **GitHub username**: Your GitHub handle
   - **Git signing public key**: Your SSH public key (`ssh-ed25519 ...`)
   - **1Password SSH auth key name**: Item name in 1Password for your auth key
   - **1Password signing key name**: Item name in 1Password for your signing key

4. Install packages:
   ```bash
   brew bundle --global
   ```

### Re-initializing (change profile or update values)

To change a prompted value, delete it from `~/.config/chezmoi/chezmoi.toml` and re-run:

```bash
chezmoi init --apply <your-github-username>
```

Or edit the value directly in `~/.config/chezmoi/chezmoi.toml` and run `chezmoi apply`.

## What Profiles Control

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

1. Authenticate GitHub CLI:
   ```bash
   gh auth login
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

## Understanding the HOME→Source Workflow

All dotfile changes follow this workflow:

1. **Edit** the file in your HOME directory (`~/.zshrc`, `~/.config/starship.toml`, etc.)
2. **Test** the change (reload shell, verify configuration)
3. **Sync** to chezmoi with `chezmoi add <file>`
4. **Commit** with `chezmoi git -- commit -m "description"`

**Why this workflow:** Editing in HOME lets you test immediately. Chezmoi then synchronizes changes to the source repository.

**Never edit directly in** `~/.local/share/chezmoi/` -- always edit in HOME first.

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

## Tool Verification Checklist

After setup, verify each component:

### Core System
- [ ] Shell loads without errors (`exec zsh`)
- [ ] Starship prompt displays correctly
- [ ] PATH includes `~/.local/bin`
- [ ] Leader key shortcuts work (`Ctrl+a f` opens yazi)

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

### Chezmoi
- [ ] Status command works (`chezmoi status`)
- [ ] Diff shows no unexpected changes (`chezmoi diff`)
- [ ] Can commit changes (`chezmoi git -- status`)

## Troubleshooting

### Config template changed warning

**Cause:** Your local `~/.config/chezmoi/chezmoi.toml` is missing a newly added variable.

**Fix:**
- Run `chezmoi init --apply <your-github-username>` to regenerate (chezmoi prompts for new values)
- Or add the missing key manually to `~/.config/chezmoi/chezmoi.toml` under `[data]`

### 1Password SSH signing errors

**Cause:** 1Password SSH agent is unreachable or misconfigured.

**Fix:**
1. Open and unlock the 1Password desktop app
2. Enable the SSH agent in 1Password Settings > Developer > SSH Agent
3. Confirm key names in `~/.config/chezmoi/chezmoi.toml` match (`op_auth_key_name`, `op_signing_key_name`)

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

**Cause:** Another application or terminal multiplexer captures `Ctrl+a`.

**Fix:**
1. Confirm WezTerm is active: `echo $TERM_PROGRAM` should output `WezTerm`
2. Check for conflicts in System Settings > Keyboard > Shortcuts, or a running tmux/screen session
3. Restart WezTerm (`Cmd+Q`, then relaunch)
4. Press `Ctrl+a` and look for the "LEADER" indicator in the status bar

### Tools not found

**Cause:** Homebrew packages are missing or PATH excludes Homebrew.

```bash
# Check what's missing
brew bundle check --global

# Install missing packages
brew bundle --global

# Verify PATH includes Homebrew
echo $PATH | grep homebrew
```

### Font or symbol issues

**Cause:** Nerd Font is missing or WezTerm uses the wrong font family.

```bash
# Install Nerd Font
brew install --cask font-meslo-lg-nerd-font

# Restart WezTerm, then verify font in config
grep "font.*family" ~/.wezterm.lua
```

### Workspace launch failures

**Cause:** Workspace scripts are missing or a required TUI tool is absent.

```bash
# Check workspace scripts exist
ls -la ~/.local/bin/workspace-*

# Test individual tools
yazi       # File manager
hx         # Editor
lazygit    # Git client

# Check WezTerm pane splitting works
# Ctrl+a |  (vertical split)
# Ctrl+a -  (horizontal split)
```

### Git authentication problems

**Cause:** GitHub CLI or SSH authentication is expired or misconfigured.

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
