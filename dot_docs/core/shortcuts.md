# Commands & Shortcuts Reference

Complete reference for all commands, shortcuts, and tools in the myTUI environment.

## Leader Key System (Ctrl+a)

The WezTerm leader key system provides quick access to all TUI applications and workspace management.

### Core TUI Applications

| Key | Tool | Description |
|-----|------|-------------|
| `f` | yazi | File manager with image previews |
| `e` | helix | Text editor with built-in LSP |
| `g` | lazygit | Git interface and repository management |
| `d` | lazydocker | Docker container management |
| `k` | k9s | Kubernetes cluster management |
| `a` | atac | API testing and HTTP client |
| `p` | procs | Process viewer with filtering |
| `m` | btop | System resource monitor |
| `n` | bandwhich | Network usage monitor by process |
| `u` | dust | Disk usage analyzer |
| `s` | zellij | Terminal session manager |

### Workspace Management

| Key | Action | Description |
|-----|--------|-------------|
| `w` | workspace-dev | Launch 4-pane development workspace |
| `h` | workspace-home | Launch home command center |
| `Shift+W` | project workspace | Launch project-specific workspace |
| `r` | refresh workspace | Refresh current workspace data |

### Pane Management

| Key | Action | Description |
|-----|--------|-------------|
| `\|` | Split vertically | Create vertical pane split |
| `-` | Split horizontally | Create horizontal pane split |
| `h/j/k/l` | Navigate panes | Move to left/down/up/right pane |
| `Shift+H/J/K/L` | Resize panes | Increase pane size in direction |
| `x` | Close pane | Close current pane (with confirmation) |
| `z` | Toggle zoom | Toggle pane fullscreen state |

### System Monitoring Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `m` | btop split | Open btop in right split (50%) |
| `Shift+M` | btop window | Open btop in new window |

### WezTerm Native Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+T` | New tab |
| `Cmd+W` | Close tab |
| `Cmd+1-9` | Switch to tab N |
| `Cmd+Shift+[/]` | Previous/next tab |
| `Cmd+Enter` | Toggle fullscreen |

### macOS Compatibility

| Shortcut | Action |
|----------|--------|
| `Option + Backspace` | Delete word backward |
| `Cmd + ←/→` | Jump to line start/end |
| `Option + ←/→` | Jump word backward/forward |
| `Cmd + Backspace` | Delete to line start |
| `Option + Delete` | Delete word forward |

## Workspace Commands

Quick access to preconfigured development environments.

```bash
# Home workspace (4-pane layout for system management)
workspace-home                 # Launch with file manager, claude, and jira tasks

# Development workspace (project-specific layout)
workspace-dev                  # Launch in current directory
workspace-dev myproject        # Launch for specific project
dev-workspace myproject        # Alias for workspace-dev

# Workspace management
workspace-refresh              # Refresh workspace data
```

## TUI Application Shortcuts

### Yazi (File Manager)

**Navigation & Basic Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `j/k` | Move up/down | Navigate file list |
| `h/l` | Back/forward | Go back/forward in directories |
| `gg/G` | Top/bottom | Go to top/bottom of list |
| `/` | Search | Search files |
| `n/N` | Next/previous | Next/previous search result |

**File Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Space` | Select | Select/deselect file |
| `a` | Select all | Select all files |
| `d` | Cut | Cut selected files |
| `y` | Copy | Copy selected files |
| `p` | Paste | Paste files |
| `D` | Delete | Delete permanently |
| `r` | Rename | Rename file |

**View Options**
| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Toggle preview | Toggle file preview panel |
| `t` | Selection mode | Toggle selection mode |
| `.` | Hidden files | Toggle hidden files visibility |
| `s` | Sort menu | Open sort options menu |

### Helix (Text Editor)

**Modes & Navigation**
| Key | Action | Description |
|-----|--------|-------------|
| `Esc` | Normal mode | Default mode (command mode) |
| `i` | Insert mode | Text insertion mode |
| `v` | Visual mode | Text selection mode |
| `:` | Command mode | Execute editor commands |

**Movement**
| Key | Action | Description |
|-----|--------|-------------|
| `h/j/k/l` | Basic movement | Left/down/up/right |
| `w/b` | Word movement | Word forward/backward |
| `0/$` | Line movement | Start/end of line |
| `gg/G` | Document movement | Start/end of file |

**Editing Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `v` | Start selection | Begin text selection |
| `d` | Delete | Delete selection |
| `y` | Copy (yank) | Copy selection |
| `p` | Paste | Paste after cursor |
| `u` | Undo | Undo last change |
| `Ctrl+r` | Redo | Redo last undone change |

**LSP Features**
| Key | Action | Description |
|-----|--------|-------------|
| `gd` | Go to definition | Jump to symbol definition |
| `gr` | Go to references | Show symbol references |
| `K` | Show hover | Display symbol information |
| `Space+a` | Code actions | Show available code actions |

**File & Search Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Space+f` | File picker | Open file picker |
| `Space+s` | Symbol search | Search symbols in file |
| `Space+/` | Global search | Search across project |

### Lazygit (Git Interface)

**Panel Navigation**
| Key | Action | Description |
|-----|--------|-------------|
| `Tab/Shift+Tab` | Switch panels | Move between git panels |
| `j/k` | Move up/down | Navigate current panel |
| `h/l` | Panel navigation | Move left/right between panels |

**File Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Space` | Stage/unstage | Stage or unstage file |
| `a` | Stage all | Stage all modified files |
| `d` | View diff | Show file differences |
| `e` | Edit file | Open file in editor |
| `D` | Discard changes | Discard unstaged changes |

**Commit Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `c` | Commit | Commit staged changes |
| `A` | Amend | Amend last commit |

**Remote Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `P` | Push | Push to remote repository |
| `p` | Pull | Pull from remote repository |

**Branch Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Space` | Checkout branch | Switch to branch (in branches panel) |
| `n` | New branch | Create new branch |
| `d` | Delete branch | Delete branch (in branches panel) |
| `r` | Rebase | Start rebase operation |
| `m` | Merge | Merge branch |

### Lazydocker (Docker Management)

**Navigation & Basic Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Switch panels | Move between docker panels |
| `j/k` | Move up/down | Navigate current panel |
| `Enter` | View details | Show container details/logs |

**Container Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Space` | Start/stop | Toggle container state |
| `r` | Restart | Restart container |
| `s` | Stop | Stop running container |
| `d` | Delete | Delete container |
| `e` | Exec shell | Execute shell in container |

**Monitoring & Cleanup**
| Key | Action | Description |
|-----|--------|-------------|
| `l` | View logs | Show container logs |
| `p` | Prune | Remove unused containers/images |

### K9s (Kubernetes Management)

**Resource Navigation**
| Command | Action | Description |
|---------|--------|-------------|
| `:pods` | View pods | List all pods |
| `:services` | View services | List all services |
| `:deployments` | View deployments | List all deployments |
| `:nodes` | View nodes | List cluster nodes |
| `:events` | View events | Show cluster events |

**Resource Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `d` | Delete | Delete selected resource |
| `l` | View logs | Show resource logs |
| `s` | Shell | Execute shell in pod |
| `Enter` | Details | View resource details |

### Procs (Process Monitor)

**Sorting & Navigation**
| Key | Action | Description |
|-----|--------|-------------|
| `c` | Sort by CPU | Sort processes by CPU usage |
| `m` | Sort by memory | Sort processes by memory usage |
| `p` | Sort by PID | Sort processes by process ID |
| `n` | Sort by name | Sort processes by name |

**Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `/` | Search | Search processes |
| `r` | Refresh rate | Adjust refresh rate |
| `k` | Kill process | Terminate selected process |
| `q` | Quit | Exit procs |

### Atac (API Client)

**Panel Navigation**
| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Switch panels | Move between URLs, Headers, Body, Response |
| `j/k` | Move up/down | Navigate current panel |

**Request Operations**
| Key | Action | Description |
|-----|--------|-------------|
| `Enter` | Execute | Send HTTP request |
| `n` | New request | Create new request |
| `e` | Edit field | Edit current field |
| `d` | Delete request | Remove request |

## Git & Development Commands

### Configuration Management (Chezmoi)

**Primary Workflow (HOME → Source)**
```bash
# Edit file in place
vim ~/.zshrc

# Test the changes work correctly  
source ~/.zshrc

# Add to chezmoi
chezmoi add ~/.zshrc

# Commit changes
chezmoi git -- commit -m "feat: add shell configuration"

# Push to remote
chezmoi git -- push
```

**Advanced Workflow (Source → HOME)**
```bash
# Edit source directly
chezmoi edit ~/.zshrc

# Preview changes
chezmoi diff

# Apply to HOME
chezmoi apply

# Commit changes
chezmoi git -- commit -m "feat: update shell configuration"
```

**Synchronization Commands**
```bash
chezmoi update               # Pull latest and apply
chezmoi status              # Check for changes
chezmoi doctor              # Diagnose issues
```

### Jira Integration

**ACLI Commands**
```bash
# Issue management
acli issue list            # Show current issues
acli issue create          # Create new issue
acli issue view KEY-123    # View specific issue

# Claude-powered integration
claude jira search         # AI-powered issue search
claude jira create         # AI-assisted issue creation
```

**Web Interface**: [middledata.atlassian.net](https://middledata.atlassian.net)

### GitHub Integration

```bash
gh dash                    # GitHub dashboard
gh issue list              # List GitHub issues
gh pr list                 # List pull requests
```

### Git Operations in HOME Directory

When in HOME directory, git commands operate on the chezmoi repository:

```bash
cd ~                       # Git prompt shows chezmoi status
git status                # Shows chezmoi repo status  
git log --oneline -10     # Recent chezmoi commits
git diff                  # Changes in chezmoi repo
```

## System Commands

### Universal Exit Commands

| Command | Application | Description |
|---------|-------------|-------------|
| `q` | Most TUI apps | Quit application |
| `Ctrl+c` | Universal | Force quit |
| `:q` | Vim-style | Quit (helix, etc.) |
| `Ctrl+a x` | WezTerm | Close pane |

### Session Management (Zellij)

```bash
zellij list-sessions          # Show active sessions
zellij attach session-name   # Reconnect to session
zellij kill-session name     # Terminate session
```

### Terminal Setup Commands

```bash
# Font installation
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# Shell restart
exec zsh                      # Restart shell
```

## Configuration Files & Paths

### Key Configuration Locations

```
~/.config/
├── starship.toml          # Prompt configuration
├── wezterm/wezterm.lua    # Terminal settings and leader keys
├── helix/config.toml      # Editor configuration
└── yazi/yazi.toml         # File manager settings

~/.local/bin/              # Custom scripts
├── workspace-home         # Home workspace launcher
├── workspace-dev          # Development workspace launcher  
└── dev-workspace          # Alias for workspace-dev

~/.local/share/chezmoi/    # Dotfiles source directory
└── .git/                  # Dotfiles repository
```

### Important Settings

**Starship Prompt**:
- Git status integration for all repositories
- Performance optimized (sub-200ms rendering)
- Custom HOME directory integration for chezmoi

**WezTerm Leader Key**:
- Leader key: `Ctrl+a`
- Timeout: 1000ms
- Visual feedback on leader key press

**Jira Integration**:
- Atlassian CLI (ACLI) for command-line access
- Claude Code MCP integration for AI-powered task management
- Web interface integration via middledata.atlassian.net

### Environment Variables

```bash
# Chezmoi
CHEZMOI_SOURCE_DIR="$HOME/.local/share/chezmoi"

# Editor preference
EDITOR="hx"                    # Default to helix
VISUAL="hx"

# Path additions
PATH="$HOME/.local/bin:$PATH"  # Custom scripts

# Tool-specific
JIRA_API_TOKEN="$(op read ...)" # Jira authentication token
```

## Troubleshooting Quick Reference

### Common Issues & Solutions

**Chezmoi sync problems:**
```bash
chezmoi doctor              # Diagnose configuration issues
chezmoi status              # Check for uncommitted changes
chezmoi diff                # Review pending changes
```

**WezTerm leader key not working:**
- Check if timeout expired (1000ms)
- Verify no conflicting key bindings
- Restart WezTerm if necessary

**TUI application crashes:**
```bash
# Reset terminal state
reset

# Clear problematic settings
unset TERM_PROGRAM_VERSION

# Restart with clean environment
exec zsh
```

**Git authentication issues:**
```bash
# Verify SSH agent
ssh-add -l

# Test GitHub connection
ssh -T git@github.com

# Check 1Password SSH agent
op account list
```

**Performance issues:**
```bash
# Check system resources
Ctrl+a m                    # Open btop monitor

# Monitor network usage
Ctrl+a n                    # Open bandwhich

# Check disk usage
Ctrl+a u                    # Open dust analyzer
```

---

*For detailed workflow documentation → [workflows guide](workflows.md)*
*For tool-specific advanced usage → [applications guide](applications.md)*