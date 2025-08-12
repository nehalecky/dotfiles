# Reference Guide

Complete reference for all commands, shortcuts, and tools in the myTUI environment.

## Shortcuts

### Leader Key Combinations (`Ctrl+a` + key)

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
| `h` | workspace-home | Launch home workspace |
| `w` | workspace-dev | Launch 4-pane development workspace |

### WezTerm Native Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+T` | New tab |
| `Cmd+W` | Close tab |
| `Cmd+1-9` | Switch to tab N |
| `Cmd+Shift+[/]` | Previous/next tab |

*For workspace management workflows → [workflows guide](workflows.md#workspace-management)*

## Commands

### Workspace Management

```bash
# Home workspace (4-pane layout for system management)
workspace-home                 # Launch with file manager, claude, and tasks

# Development workspace (project-specific layout)
workspace-dev                  # Launch in current directory
workspace-dev myproject        # Launch for specific project
dev-workspace myproject        # Alias for workspace-dev
```

### Configuration Management

```bash
# Primary workflow (HOME → Source)
vim ~/.zshrc                   # Edit file in place
chezmoi add ~/.zshrc          # Add to chezmoi
chezmoi git -- commit -m ""   # Commit changes
chezmoi git -- push          # Push to remote

# Advanced workflow (Source → HOME)  
chezmoi edit ~/.zshrc         # Edit source directly
chezmoi diff                  # Preview changes
chezmoi apply                 # Apply to HOME
chezmoi git -- commit -m ""  # Commit changes

# Synchronization
chezmoi update               # Pull latest and apply
chezmoi status              # Check for changes
chezmoi doctor              # Diagnose issues
```

### Task Management

```bash
# Basic task operations
task add "Description" +tag priority:H due:tomorrow
task list                   # Show all pending tasks
task next                  # Show most urgent tasks (limit 10)
task done 1                # Mark task 1 as completed

# Custom reports
task work                  # Show work-tagged tasks only
task personal              # Show personal-tagged tasks only

# Task modification
task 1 modify priority:L   # Change priority
task 1 modify +urgent      # Add urgent tag
task 1 annotate "note"     # Add annotation
```

### Git Integration

When in HOME directory, git commands operate on the chezmoi repository:

```bash
cd ~                       # Git prompt shows chezmoi status
git status                # Shows chezmoi repo status  
git log --oneline -10     # Recent chezmoi commits
git diff                  # Changes in chezmoi repo
```

*Learn more about [dotfile workflows →](workflows.md#dotfile-management)*

## Tools

### File Management

**yazi** - Terminal file manager
- **Navigation**: `hjkl` vim keys, `gg/G` top/bottom
- **Operations**: `yy` copy, `dd` cut, `pp` paste, `DD` delete
- **Preview**: Images, PDFs, code with syntax highlighting
- **Search**: `/` to search, `n/N` next/previous

### Text Editing

**helix** - Post-modern text editor
- **Mode**: Normal by default (like vim)
- **Navigation**: `hjkl` movement, `w/b` word, `gg/ge` document
- **Selection**: `v` visual, `V` line, `C-v` block
- **LSP**: Built-in language server support, no configuration needed
- **Multi-cursor**: `C` add cursor, `Alt-C` add all matches

### Git Management

**lazygit** - Terminal git interface
- **Navigation**: `hjkl` or arrow keys
- **Staging**: `space` stage/unstage, `a` stage all
- **Commits**: `c` commit, `C` commit with message
- **Branches**: `b` branch menu, `P` push, `p` pull
- **Merge**: `m` merge, `r` rebase

### Container Management

**lazydocker** - Docker TUI
- **Navigation**: `hjkl` or arrow keys between panels
- **Actions**: `enter` view details, `d` delete, `r` restart
- **Logs**: `l` view logs, `s` search logs
- **Stats**: Real-time container resource usage

### API Testing

**atac** - Terminal API client
- **Requests**: Create HTTP requests with headers and body
- **Collections**: Organize requests into collections
- **Environment**: Variable substitution support
- **Response**: View formatted JSON, headers, timing

### System Monitoring

**btop** - Resource monitor
- **CPU**: Per-core usage with history graphs
- **Memory**: RAM and swap usage visualization  
- **Processes**: Sortable process list with filtering
- **Network**: Real-time network I/O statistics

**bandwhich** - Network monitor
- **Process**: Network usage by process
- **Remote**: Connections by remote address
- **Protocol**: Traffic breakdown by protocol

**dust** - Disk usage
- **Tree**: Directory size visualization
- **Sorting**: By size, with percentages
- **Navigation**: Interactive directory exploration

### Task Management

**taskwarrior-tui** - Interactive task manager
- **Navigation**: `j/k` move up/down, `enter` select
- **Actions**: `a` add task, `d` mark done, `e` edit
- **Filtering**: `/` filter, `esc` clear filter
- **Help**: `?` show all keybindings

**Task Tags with Colors**:
- `+urgent` - Red highlight for high priority items
- `+work` - Orange highlight for work-related tasks  
- `+personal` - Blue highlight for personal tasks
- Custom priorities: `H` (high), `M` (medium), `L` (low)

## Configuration Files

### Key Configuration Locations

```
~/.config/
├── starship.toml          # Prompt configuration
├── wezterm/wezterm.lua    # Terminal settings and leader keys
├── helix/config.toml      # Editor configuration
├── yazi/yazi.toml         # File manager settings
└── task/taskrc            # Task management configuration

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

**Taskwarrior**:
- Custom urgency coefficients for smart sorting
- Color-coded priority and tag system
- Custom reports for work/personal task filtering

*For customization details → [workflows guide](workflows.md#customization)*

## Environment Variables

Key environment variables that affect myTUI behavior:

```bash
# Chezmoi
CHEZMOI_SOURCE_DIR="$HOME/.local/share/chezmoi"

# Editor preference
EDITOR="hx"                    # Default to helix
VISUAL="hx"

# Path additions
PATH="$HOME/.local/bin:$PATH"  # Custom scripts

# Tool-specific
TASKDATA="$HOME/.task"         # Taskwarrior data location
```

*Configuration management details → [workflows guide](workflows.md#configuration-management)*