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
workspace-home                 # Launch with file manager, claude, and jira tasks

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

### Jira Integration

```bash
# Jira task management via ACLI
acli issue list            # Show current issues
acli issue create          # Create new issue
acli issue view KEY-123    # View specific issue

# Claude-powered Jira integration
claude jira search         # AI-powered issue search
claude jira create         # AI-assisted issue creation

# GitHub integration
gh dash                    # GitHub dashboard
gh issue list              # List GitHub issues
gh pr list                 # List pull requests
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

### Jira Integration

**Web Interface**: [middledata.atlassian.net](https://middledata.atlassian.net)
- Full-featured Jira interface for comprehensive task management
- Board views, sprint planning, and project tracking
- Integration with GitHub via pull request links

**ACLI Commands**:
- **Issue Management**: Create, view, edit, and transition issues
- **Project Access**: List projects, view boards and sprints
- **Search**: JQL-powered advanced searching
- **Integration**: Works with Claude Code for AI assistance

**Active Projects**:
- **INT Project** - Main integration and automation tasks
- **GitHub Stars Migration** - Repository organization project
- **Weather TUI Enhancement** - Terminal interface improvements

## Configuration Files

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
- Seamless web interface integration via middledata.atlassian.net

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
JIRA_API_TOKEN="$(op read ...)" # Jira authentication token
```

*Configuration management details → [workflows guide](workflows.md#configuration-management)*