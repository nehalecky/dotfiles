# Setup Guide

First-time setup, customization, and configuration for this development environment.

## Quick Install

### Prerequisites

- macOS 14+ (tested on Apple silicon and Intel)
- Administrative access for Homebrew installation
- Internet connection for downloading tools
- GitHub account for dotfiles repository access

### Bootstrap Installation

1. **Install Homebrew package manager**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install chezmoi and deploy dotfiles** (includes all 67+ tools):
   ```bash
   brew install chezmoi && chezmoi init --apply https://github.com/nehalecky/dotfiles.git
   ```

3. **Restart your terminal** to load new configurations and launch first workspace:
   ```bash
   workspace-home
   ```

This single command installs and configures:
- Shell environment (zsh, prezto, starship prompt)
- Terminal multiplexer (WezTerm with leader key shortcuts)
- Development tools (git, GitHub CLI, language runtimes)
- TUI applications (file manager, editor, git client, system monitors)
- Authentication (1Password SSH agent integration)

## First-Time Setup

### Terminal Configuration

After installation, verify your terminal environment is configured correctly.

**Shell Environment:**
```bash
# Verify zsh is your default shell
echo $SHELL                    # Should output: /bin/zsh

# Check starship prompt loads
starship --version             # Should display version number

# Verify PATH includes local binaries
echo $PATH | grep ".local/bin" # Should find ~/.local/bin
```

**Leader Key System:**

WezTerm uses `Ctrl+a` as the leader key for all shortcuts. Test the system:

```bash
# Press Ctrl+a, then f - should open yazi file manager
# Press Ctrl+a, then g - should open lazygit
# Press Ctrl+a, then e - should open helix editor

# If nothing happens:
# 1. Verify you're running WezTerm (not another terminal)
# 2. Check no other app is capturing Ctrl+a
# 3. Restart WezTerm: Cmd+Q then relaunch
```

**Font Verification:**

The configuration uses MesloLGS NF (Nerd Font) for icons and symbols:

```bash
# If you see missing symbols or boxes, install the font:
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# Restart WezTerm after installation
```

### Authentication Setup

**1Password SSH Agent:**

Configure SSH authentication through 1Password for secure, biometric-enabled access:

1. Open 1Password app
2. Navigate to Settings → Developer
3. Enable "Use the SSH agent"
4. Add your SSH keys to 1Password

Verify SSH agent is working:
```bash
ssh-add -L                     # Should list your SSH keys from 1Password
```

**GitHub CLI Authentication:**

Set up GitHub CLI for repository operations:

```bash
# Authenticate GitHub CLI
gh auth login

# Configure git to use GitHub CLI
gh auth setup-git

# Verify authentication
gh auth status
```

### Development Tools Verification

Test that core development tools are installed and working:

**Python Development (uv):**
```bash
uv --version                   # Python package manager
python3 --version              # System Python
```

**Node.js Development:**
```bash
node --version
npm --version
```

**Git Configuration:**
```bash
git config --global user.name
git config --global user.email
git config --global commit.gpgsign  # Should be true for SSH signing
```

**TUI Tools:**
```bash
# Test launching individual tools
yazi --version                 # File manager
hx --version                   # Helix editor (also 'helix')
lazygit --version              # Git client
btop --version                 # System monitor
```

### Workspace System

The workspace system provides pre-configured multi-pane environments.

**Home Workspace (Command Center):**
```bash
workspace-home
```

This launches a 4-pane layout for daily operations:
- Terminal (zsh) - System commands and dotfiles management
- File Manager (yazi) - Browse files and configurations
- Claude Code - AI-assisted development
- Task Management - Jira integration and system tools

**Development Workspace (Project Work):**
```bash
cd /path/to/project
workspace-dev                  # Uses current directory name

# OR specify project name
workspace-dev myproject
```

This launches a 4-pane layout for development:
- Terminal/REPL - Run commands, tests, build tools
- Editor (Helix) - Code editing with LSP support
- Git (lazygit) - Version control operations
- Monitor/Tests - Project-specific tools and output

**Verify Workspaces:**
```bash
# Test home workspace launches
workspace-home
# Press 'q' in each pane to exit

# Test development workspace launches
workspace-dev test-project
# Exit all panes
```

## Customization

### Understanding the HOME → Source Workflow

All dotfile changes follow a consistent workflow:

1. **Edit** actual files in your HOME directory (`~/.zshrc`, `~/.config/starship.toml`, etc.)
2. **Test** changes work correctly (reload shell, test configuration)
3. **Sync** to chezmoi with `chezmoi add <file>`
4. **Commit** changes with `chezmoi git -- commit -m "description"`

**Why this workflow**: Direct editing ensures immediate testing. Chezmoi handles synchronization to the source repository.

**Never edit directly in** `~/.local/share/chezmoi/` - always edit in HOME first.

### Adding Custom Configurations

**Shell Configuration:**

Customize your shell environment by editing `~/.zshrc`:

```bash
# Edit the file
vim ~/.zshrc

# Test changes work
source ~/.zshrc

# Add to chezmoi
chezmoi add ~/.zshrc

# Commit changes
chezmoi git -- commit -m "feat: add custom shell aliases"

# Push to remote
chezmoi git -- push
```

**Starship Prompt:**

Customize your prompt appearance:

```bash
# Edit starship configuration
vim ~/.config/starship.toml

# Preview changes (restart prompt automatically applies)
exec zsh

# Sync to chezmoi
chezmoi add ~/.config/starship.toml
chezmoi git -- commit -m "style: customize prompt appearance"
```

**WezTerm Shortcuts:**

Add new leader key shortcuts:

```bash
# Edit WezTerm configuration
vim ~/.wezterm.lua

# Find the leader_key_bindings table and add:
# { key = 'x', action = wezterm.action.SpawnCommandInNewTab {
#   args = { 'your-command' },
# }},

# Test the shortcut: Ctrl+a, then x
# If it works, sync to chezmoi
chezmoi add ~/.wezterm.lua
chezmoi git -- commit -m "feat: add custom WezTerm shortcut"
```

### Tool Preferences

Most development tools store configuration in `~/.config/`:

**File Manager (yazi):**
```bash
vim ~/.config/yazi/yazi.toml   # Behavior settings
vim ~/.config/yazi/theme.toml  # Visual appearance
```

**Editor (helix):**
```bash
vim ~/.config/helix/config.toml       # Keybindings, theme, LSP settings
vim ~/.config/helix/languages.toml    # Language server configurations
```

**Git Client (lazygit):**
```bash
vim ~/.config/lazygit/config.yml      # Keybindings and appearance
```

After editing any config file:
```bash
# Test the changes work
# Then sync to chezmoi
chezmoi add ~/.config/tool/config.file
chezmoi git -- commit -m "chore: customize tool settings"
```

### Creating Custom Scripts

Add your own utility scripts to `~/.local/bin/`:

```bash
# Create new script (in HOME, not chezmoi source)
vim ~/.local/bin/my-script

# Make executable
chmod +x ~/.local/bin/my-script

# Test it works
my-script

# Add to chezmoi
chezmoi add ~/.local/bin/my-script

# Commit
chezmoi git -- commit -m "feat: add custom utility script"
```

Scripts in `~/.local/bin/` are automatically in your PATH.

### Machine-Specific Settings

Use `.chezmoidata.yaml` for values that differ between machines:

```bash
# Edit machine-specific data
vim ~/.local/share/chezmoi/.chezmoidata.yaml
```

Example configuration:
```yaml
email: "work@example.com"
work_mode: true
theme: "dark"
```

Reference these values in template files (`.tmpl` extension):
```toml
# ~/.config/starship.toml.tmpl
{{- if .work_mode }}
[custom.work_indicator]
command = "echo 'WORK'"
{{- end }}
```

Apply templates:
```bash
chezmoi apply --force          # Regenerate templated files
```

### Advanced Workflow: Source → HOME

For complex batch changes across multiple files:

```bash
# Edit source files directly
chezmoi edit ~/.zshrc          # Opens source file in editor

# Preview what would change
chezmoi diff

# Apply changes to HOME
chezmoi apply

# Test changes
source ~/.zshrc

# Commit if satisfied
chezmoi git -- commit -m "refactor: reorganize shell configuration"
```

**When to use**: Making coordinated changes to multiple files, or when you need to preview templated output before applying.

## Multi-Machine Synchronization

### Pulling Changes from Another Machine

**Quick update (pull + apply):**
```bash
chezmoi update                 # Pull latest from remote and apply
```

**Manual sync with review:**
```bash
chezmoi git pull              # Pull latest changes
chezmoi diff                  # Review what will change
chezmoi apply                 # Apply changes to HOME
```

### Pushing Changes to Other Machines

```bash
# From the machine where you made changes
chezmoi git -- push

# On other machines
chezmoi update                # Pull and apply automatically
```

### Syncing Specific Configurations

```bash
# Pull only dotfiles, don't apply
chezmoi git pull

# Apply only specific files
chezmoi apply ~/.zshrc
chezmoi apply ~/.config/starship.toml

# Review before applying everything
chezmoi diff
chezmoi apply
```

## Tool Verification Checklist

After setup, verify everything works:

### Core System
- [ ] Shell loads without errors (`exec zsh`)
- [ ] Starship prompt displays correctly
- [ ] PATH includes `~/.local/bin`
- [ ] Leader key shortcuts work (`Ctrl+a f` opens yazi)

### Authentication
- [ ] 1Password SSH agent working (`ssh-add -L`)
- [ ] GitHub CLI authenticated (`gh auth status`)
- [ ] Git signing configured (`git config commit.gpgsign`)

### Development Tools
- [ ] Python/uv installed (`uv --version`)
- [ ] Node.js installed (`node --version`)
- [ ] Git configured with name and email

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

### Leader Key Not Working

**Symptoms**: Pressing `Ctrl+a` followed by shortcut keys does nothing.

**Solutions**:
1. Verify you're running WezTerm: `echo $TERM_PROGRAM` should output `WezTerm`
2. Check if another application captures `Ctrl+a`:
   - System keyboard shortcuts (System Settings → Keyboard → Shortcuts)
   - Other terminal multiplexers (tmux/screen running?)
3. Restart WezTerm: `Cmd+Q` then relaunch
4. Check WezTerm configuration loaded: Look for "LEADER" indicator in status bar when pressing `Ctrl+a`

### Tools Not Found

**Symptoms**: Commands like `yazi`, `lazygit`, or `hx` return "command not found".

**Solutions**:
```bash
# Check what's missing
brew bundle check

# Install missing packages
brew bundle install

# Verify PATH includes Homebrew
echo $PATH | grep homebrew
```

### Chezmoi Sync Issues

**Symptoms**: Changes not syncing, unexpected diffs, or conflicts.

**Solutions**:
```bash
# Diagnose configuration
chezmoi doctor

# Check current status
chezmoi status

# See specific differences
chezmoi diff

# Force apply (overwrites HOME with source)
chezmoi apply --force

# Reset to clean state (careful!)
chezmoi git -- reset --hard origin/master
chezmoi apply
```

### Font or Symbol Issues

**Symptoms**: Boxes, missing icons, or garbled text in prompt or TUI tools.

**Solutions**:
```bash
# Install Nerd Font
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# Restart WezTerm
# Verify font in WezTerm config
grep "font.*family" ~/.wezterm.lua
```

### Workspace Launch Failures

**Symptoms**: `workspace-home` or `workspace-dev` commands fail or hang.

**Solutions**:
```bash
# Check workspace scripts exist
ls -la ~/.local/bin/workspace-*

# Test individual commands
yazi                          # Should launch file manager
hx                            # Should launch editor
lazygit                       # Should launch git client

# Check WezTerm multiplexing works
Ctrl+a |                      # Should split pane vertically
Ctrl+a -                      # Should split pane horizontally
```

### Git Authentication Problems

**Symptoms**: Git push/pull asks for credentials, or fails with authentication errors.

**Solutions**:
```bash
# Check GitHub CLI status
gh auth status

# Re-authenticate if needed
gh auth login

# Ensure git uses GitHub CLI
gh auth setup-git

# Test SSH to GitHub
ssh -T git@github.com
```

### 1Password SSH Issues

**Symptoms**: SSH operations hang or fail, no Touch ID prompt.

**Solutions**:
1. Ensure 1Password app is running
2. Check SSH agent configuration:
   ```bash
   ssh-add -L                # Should list keys from 1Password
   echo $SSH_AUTH_SOCK       # Should point to 1Password socket
   ```
3. Restart 1Password app
4. Verify SSH agent enabled in 1Password Settings → Developer

### Performance Issues

**Slow prompt rendering:**
```bash
# Diagnose starship performance
starship timings

# Disable expensive modules temporarily
vim ~/.config/starship.toml
# Comment out slow modules (git status, package version, etc.)
```

**High CPU usage:**
```bash
# Check running processes
btop                          # Or Ctrl+a p

# Look for runaway processes
# Exit unused TUI applications with 'q'
```

**Memory usage:**
```bash
# Exit unused applications
# Restart WezTerm periodically for cleanup
Cmd+Q                         # Quit WezTerm
# Relaunch
```

## Next Steps

After completing setup and customization:

- **[Tool Reference](tool-reference.md)** - Complete command and shortcut reference for all TUI tools
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions
- **[README](README.md)** - Overview and philosophy
- **[CLAUDE.md](../CLAUDE.md)** - Development workflows and coding standards

### Quick Reference

**Daily Commands:**
```bash
workspace-home                # Launch home workspace
workspace-dev project         # Launch development workspace
chezmoi add ~/.file           # Sync changed file
chezmoi git -- commit -m "msg" # Commit changes
chezmoi update                # Pull latest configs
```

**Essential Shortcuts:**
```bash
Ctrl+a f                      # File manager (yazi)
Ctrl+a e                      # Editor (helix)
Ctrl+a g                      # Git client (lazygit)
Ctrl+a p                      # System monitor (btop)
Ctrl+a |                      # Split pane vertical
Ctrl+a -                      # Split pane horizontal
```

**Getting Help:**
```bash
chezmoi doctor                # Diagnose chezmoi issues
brew doctor                   # Diagnose Homebrew issues
gh auth status                # Check GitHub authentication
tool --help                   # Help for any command
?                             # Help in most TUI applications
```
