# Daily Workflows

Practical guides for common tasks and daily development patterns.

## Installation

### Prerequisites

- macOS (tested on macOS 14+)
- Administrative access for Homebrew installation
- Internet connection for downloading tools

### Step-by-Step Setup

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Initialize dotfiles**:
   ```bash
   brew install chezmoi
   chezmoi init --apply nehalecky/dotfiles
   ```

3. **Install all tools**:
   ```bash
   cd ~/.local/share/chezmoi
   brew bundle install
   ```

4. **Restart your terminal** to load new configurations

5. **Launch first workspace**:
   ```bash
   workspace-home
   ```

### Verification

After setup, verify core functionality:

```bash
# Test leader key shortcuts
# Press Ctrl+a, then f - should open yazi file manager
# Press Ctrl+a, then g - should open lazygit

# Verify prompt integration
cd ~                          # Should show chezmoi git status in prompt
chezmoi status               # Should show configuration status
```

*For troubleshooting → [see troubleshooting section](#troubleshooting)*

## Workspace Management

### Home Workspace

Launch your daily command center:

```bash
workspace-home
```

**Layout**:
```
┌─────────────────┬─────────────────┐
│ Terminal (zsh)  │ Files (yazi)    │
│ HOME directory  │ File browser    │
├─────────────────┼─────────────────┤
│ Claude Code     │ Tasks (tw-tui)  │
│ AI assistance   │ Task management │
└─────────────────┴─────────────────┘
```

**Purpose**: System administration, configuration management, task tracking, and AI-assisted development.

### Development Workspace

Launch project-specific development environment:

```bash
workspace-dev myproject       # Create workspace for 'myproject'
cd /path/to/project && workspace-dev  # Use current directory name
```

**Auto-detected Project Types**:
- **Python**: Shows `uv` dependency tree, activates virtual environment
- **Node.js**: Displays npm scripts, suggests `npm run dev`
- **Rust**: Shows cargo commands, suggests `cargo watch`
- **Go**: Shows module info, suggests `go run .`

**Layout**:
```
┌─────────────────┬─────────────────┐
│ Terminal        │ Editor (helix)  │
│ Project root    │ Code editing    │
├─────────────────┼─────────────────┤
│ Git (lazygit)   │ Monitor/Tools   │
│ Version control │ Project-specific│
└─────────────────┴─────────────────┘
```

*Complete shortcuts reference → [reference guide](reference.md#shortcuts)*

## Dotfile Management

### Understanding the HOME Integration

When you're in your HOME directory, the git prompt shows your dotfiles repository status due to a symlink from `~/.git` to `~/.local/share/chezmoi/.git`.

**Prompt Indicators**:
- `master` - Current branch name
- `✘` - Modified files (unstaged changes)
- `?` - Untracked files  
- `+` - Staged changes
- `⇡N` - N commits ahead of remote
- `⇣N` - N commits behind remote

### Primary Workflow: HOME → Source

**Use this for daily configuration changes**:

```bash
# 1. Edit configuration file directly
vim ~/.zshrc                   # Edit in place

# 2. Test the changes
source ~/.zshrc               # Verify changes work

# 3. Add to chezmoi
chezmoi add ~/.zshrc          # Sync to dotfiles repository

# 4. Commit changes  
chezmoi git -- commit -m "Update shell configuration"

# 5. Push to remote
chezmoi git -- push
```

**Why this workflow**: Direct editing ensures immediate testing, and chezmoi handles the synchronization.

### Advanced Workflow: Source → HOME

**Use this for complex batch changes**:

```bash
# 1. Edit source file directly
chezmoi edit ~/.zshrc         # Opens source file in editor

# 2. Preview changes
chezmoi diff                  # See what would change

# 3. Apply changes
chezmoi apply                 # Update HOME directory files

# 4. Test changes
source ~/.zshrc               # Verify functionality

# 5. Commit if satisfied
chezmoi git -- commit -m "Batch update shell configuration"
```

**When to use**: Making changes to multiple files, or when you need to see the templated output before applying.

### Multi-Machine Synchronization

**Pull latest changes**:
```bash
chezmoi update                # Pull from remote and apply
```

**Manual sync process**:
```bash
chezmoi git pull             # Pull latest changes
chezmoi diff                 # Review incoming changes
chezmoi apply                # Apply changes to HOME
```

*For complete command reference → [reference guide](reference.md#commands)*

## Configuration Management

### Customization Principles

1. **Test locally first** - Always verify changes work before committing
2. **Use templates for machine-specific values** - Store variations in `.chezmoidata.yaml`
3. **Document complex configurations** - Add comments explaining non-obvious choices
4. **Version everything** - All configuration should be tracked

### Common Customizations

**Adding new leader key shortcuts**:

1. Edit WezTerm configuration:
   ```bash
   chezmoi edit ~/.config/wezterm/wezterm.lua
   ```

2. Add new key binding in the `leader_key_bindings` table:
   ```lua
   { key = 'x', action = wezterm.action.SpawnCommandInNewTab {
     args = { 'your-command' },
   }},
   ```

3. Apply and test:
   ```bash
   chezmoi apply
   # Test: Press Ctrl+a, then x
   ```

**Modifying tool configurations**:

Most tool configurations are in `~/.config/`:
- `starship.toml` - Prompt appearance and modules
- `helix/config.toml` - Editor keybindings and LSP settings
- `yazi/yazi.toml` - File manager behavior and previews
- `task/taskrc` - Task management rules and colors

**Adding custom scripts**:

1. Create script in `~/.local/bin/`:
   ```bash
   chezmoi edit ~/.local/bin/my-script
   ```

2. Make executable and add to chezmoi:
   ```bash
   chezmoi apply
   chmod +x ~/.local/bin/my-script
   chezmoi add ~/.local/bin/my-script
   ```

### Machine-Specific Settings

Use `.chezmoidata.yaml` for values that differ between machines:

```yaml
# ~/.local/share/chezmoi/.chezmoidata.yaml
email: "work@example.com"
work_mode: true
```

Then reference in templates:
```toml
# ~/.config/starship.toml.tmpl
{{- if .work_mode }}
[custom.work_indicator]
command = "echo 'WORK'"
{{- end }}
```

## Task Management

### Daily Task Workflow

**Adding tasks**:
```bash
task add "Review PR #123" +work priority:H due:today
task add "Grocery shopping" +personal due:weekend
task add "Deploy feature" +work +urgent
```

**Viewing tasks**:
```bash
task list                    # All pending tasks
task next                    # Most urgent 10 tasks
task work                    # Work tasks only
task personal                # Personal tasks only
```

**Managing tasks**:
```bash
task 1 done                  # Mark task 1 complete
task 2 modify priority:L     # Lower priority
task 3 modify +urgent        # Add urgent tag
task 4 annotate "blocked by API issue"  # Add note
```

### Taskwarrior-TUI Usage

Launch with `taskwarrior-tui` or via home workspace (`workspace-home`).

**Key bindings**:
- `a` - Add new task
- `d` - Mark selected task done
- `e` - Edit task details
- `j/k` - Navigate up/down
- `/` - Filter tasks by text
- `?` - Show help

### Custom Task Reports

**Work tasks** (`task work`):
- Shows only tasks tagged with `+work`
- Sorted by priority then due date
- Useful for focusing during work hours

**Personal tasks** (`task personal`):
- Shows only tasks tagged with `+personal`  
- Sorted by priority then due date
- Good for weekend/personal time planning

*Complete task management reference → [reference guide](reference.md#task-management)*

## Troubleshooting

### Common Issues

**Leader key not working**:
1. Verify WezTerm is running (not another terminal)
2. Check if another application is capturing `Ctrl+a`
3. Try restarting WezTerm: `Cmd+Q` then relaunch

**Tools not found**:
```bash
brew bundle check            # See what's missing
brew bundle install          # Install missing packages
```

**Chezmoi sync issues**:
```bash
chezmoi doctor               # Diagnose configuration issues
chezmoi status               # Check what's changed
chezmoi diff                 # See specific differences
```

**Git authentication problems**:
```bash
gh auth status               # Check GitHub CLI authentication
gh auth login                # Re-authenticate if needed
```

**1Password SSH issues**:
1. Ensure 1Password app is running
2. Check SSH agent configuration:
   ```bash
   ssh-add -L                # List loaded keys
   ```
3. Restart 1Password if needed

### Performance Issues

**Slow prompt**:
- Check starship modules are optimized
- Verify git repositories aren't too large
- Consider disabling expensive prompt modules temporarily

**High CPU usage**:
- Check `btop` to identify resource-heavy processes
- Verify no runaway background tasks from TUI tools

**Memory usage**:
- Exit unused TUI applications with `q`
- Restart WezTerm periodically for memory cleanup

### Getting Help

**Documentation**:
- [Reference guide](reference.md) - Complete command and shortcut reference
- [README](../README.md) - Overview and quick start

**Diagnostics**:
```bash
chezmoi doctor               # Configuration health check
brew doctor                  # Homebrew diagnostics  
gh auth status              # GitHub authentication status
op signin --account <account> # 1Password CLI authentication
```

**Community**:
- Individual tool documentation (run `tool --help`)
- GitHub issues for tool-specific problems
- chezmoi documentation for dotfile management issues

*Back to [README](../README.md) • [Reference](reference.md)*