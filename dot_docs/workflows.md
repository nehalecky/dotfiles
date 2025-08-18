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
│ Claude Code     │ Jira Tasks      │
│ AI assistance   │ & System Mgmt   │
└─────────────────┴─────────────────┘
```

**Purpose**: System administration, configuration management, Jira task management, and AI-assisted development.

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

### Jira Integration Workflow

**Task Management via Jira**:
- All business and project tasks managed in Jira at **middledata.atlassian.net**
- Access via web interface or ACLI command line tool
- Integration with Claude Code for AI-assisted task management

**Daily commands**:
```bash
acli issue list              # View current Jira issues
acli issue create            # Create new issue
claude jira search           # AI-powered Jira search via Claude
gh dash                      # GitHub dashboard for PRs/issues

# Claude Code AI Development Integration
python3 ~/.claude/memories/templates/generator.py .  # Generate/refresh project CLAUDE.md
```

**Active Projects in Jira**:
- **INT-7**: GitHub Stars Migration (26 batch tasks)
- **INT-24**: Weather TUI Project (12 enhancement tasks)
- **INT-35**: Omnara AI Evaluation
- **INT-36**: Weather Forecast Enhancement

### Home Workspace Integration

The home workspace automatically displays:
- Quick Jira commands and shortcuts
- System management tools
- GitHub dashboard integration
- Migration success confirmation

**Jira Web Access**: [middledata.atlassian.net](https://middledata.atlassian.net)

*Complete Jira integration reference → [reference guide](reference.md#jira-integration)*

## Memory System Management

### Daily AI Context Operations

**Generate/refresh project CLAUDE.md**:
```bash
cd /path/to/project
python3 ~/.claude/memories/templates/generator.py .
```

**Update memory modules**:
```bash
# Edit shared modules that affect all projects
vim ~/.claude/memories/tools/essential-tools.md
vim ~/.claude/memories/stacks/python.md

# Commit changes through chezmoi
chezmoi add ~/.claude/memories/
chezmoi git -- commit -m "update: improve memory module documentation"
chezmoi git -- push
```

**Sync memory system across machines**:
```bash
chezmoi update                # Pull latest and apply
# OR manually:
chezmoi git pull             # Pull changes
chezmoi diff                 # Review memory system changes  
chezmoi apply                # Apply to ~/.claude/memories/
```

### Quick Memory System Health Check

```bash
# Verify memory system exists
ls ~/.claude/memories/

# Check project CLAUDE.md imports
grep '^@' CLAUDE.md

# Validate a project's memory imports
python3 -c "
from pathlib import Path
import sys
sys.path.append(str(Path.home() / '.claude/memories/templates'))
from generator import ProjectDetector
detector = ProjectDetector(Path('.'))
print('Project type:', detector.detect().type)
"
```

*For complete memory system guide → [Claude Memory System](claude-memory-system.md)*

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

**Memory system issues**:
```bash
# Check memory system directory
ls -la ~/.claude/memories/

# Verify project generator works
python3 ~/.claude/memories/templates/generator.py --help

# Regenerate project CLAUDE.md
python3 ~/.claude/memories/templates/generator.py .
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