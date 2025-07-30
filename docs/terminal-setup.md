# Terminal Setup Guide

## Overview

This repository implements an ultra-modern terminal-first development environment:
- **WezTerm** - GPU-accelerated terminal with advanced multiplexing
- **Starship** - Blazing fast cross-shell prompt (50ms faster than P10k)
- **Zsh + Prezto** - Enhanced shell with syntax highlighting and completions
- **Modern TUI Stack** - 10+ cutting-edge terminal applications

## Modern TUI Stack

Our aggressive Phase 1 implementation includes these cutting-edge tools:

| Tool | Purpose | Leader Key | Description |
|------|---------|------------|-------------|
| **yazi** | File Manager | `Leader + f` | Blazing fast file manager with image previews |
| **helix** | Text Editor | `Leader + e` | Post-modern modal editor with built-in LSP |
| **lazygit** | Git UI | `Leader + g` | Intuitive git interface for staging, commits, branches |
| **k9s** | Kubernetes | `Leader + k` | Cluster management with real-time monitoring |
| **lazydocker** | Docker UI | `Leader + D` | Docker and docker-compose management |
| **atac** | API Client | `Leader + a` | Postman-like API testing in terminal |
| **procs** | Process Viewer | `Leader + p` | Modern replacement for ps |
| **bandwhich** | Network Monitor | `Leader + n` | Real-time bandwidth usage by process |
| **dust** | Disk Usage | `Leader + u` | Modern du with intuitive visualization |
| **zellij** | Session Manager | `Leader + s` | Modern tmux alternative |

## Key Features

### Leader Key System
- **Leader**: `Ctrl+a` (similar to tmux)
- **Timeout**: 1000ms
- **Visual indicator**: Shows "LEADER" in status bar when active

### Pane Management

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Split Vertical | `Leader + \|` | Split pane vertically |
| Split Horizontal | `Leader + -` | Split pane horizontally |
| Navigate Left | `Leader + h` | Move to pane on the left |
| Navigate Right | `Leader + l` | Move to pane on the right |
| Navigate Up | `Leader + k` | Move to pane above |
| Navigate Down | `Leader + j` | Move to pane below |
| Resize Left | `Leader + Shift + H` | Increase pane size left |
| Resize Right | `Leader + Shift + L` | Increase pane size right |
| Resize Up | `Leader + Shift + K` | Increase pane size up |
| Resize Down | `Leader + Shift + J` | Increase pane size down |
| Close Pane | `Leader + x` | Close current pane (with confirmation) |
| Zoom Toggle | `Leader + z` | Toggle pane zoom state |

### Quick Reference
- **Navigate**: `Leader + h/j/k/l` (vim-style)
- **Resize**: `Leader + Shift + H/J/K/L`
- **Close**: `Leader + x`
- **Zoom**: `Leader + z`

### System Monitoring

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Monitor Split | `Leader + m` | Open btop in right split (50%) |
| Monitor Window | `Leader + Shift + M` | Open btop in new window |
| Dev Workspace | `Leader + w` | Create 4-tile layout (see below) |

### iTerm2 Compatibility Shortcuts

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Delete Word | `Option + Backspace` | Delete word backward |
| Beginning of Line | `Cmd + ←` | Jump to line start |
| End of Line | `Cmd + →` | Jump to line end |
| Word Left | `Option + ←` | Jump word backward |
| Word Right | `Option + →` | Jump word forward |
| Delete to Beginning | `Cmd + Backspace` | Delete to line start |
| Delete Word Forward | `Option + Delete` | Delete word forward |

### Status Bar

The status bar displays:
- **Left**: Current working directory (with `~` for home)
- **Right**: LEADER indicator when leader key is active

## Configuration Details

### Font Settings
- **Font**: MesloLGS NF (Nerd Font)
- **Size**: 12pt
- **Ligatures**: Enabled (calt, clig, liga)

### Color Scheme
- Based on Monokai/iTerm2 dark theme
- Custom ANSI colors for optimal visibility
- Hyperlink detection enabled

### Window Behavior
- **Decorations**: RESIZE (for yabai compatibility)
- **Resize Increments**: Cell-based (terminal grid)
- **Initial Size**: 80x25
- **Padding**: 2px all sides

### Performance
- **GPU Acceleration**: WebGpu frontend
- **Max FPS**: 120
- **Scrollback**: 1000 lines

## Yabai Integration

WezTerm is configured to work seamlessly with yabai:
- Uses `RESIZE` window decorations to prevent gaps
- Cell-based resizing for proper grid alignment
- No additional yabai rules needed

## Customization

The configuration file is located at `~/.wezterm.lua` and is managed by chezmoi.

To modify settings:
```bash
chezmoi edit ~/.wezterm.lua
chezmoi diff
chezmoi apply
```

## Troubleshooting

### Font Not Found
If you see font warnings, ensure MesloLGS NF is installed:
```bash
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font
```

### Pane Navigation Not Working
Ensure no other applications are intercepting `Ctrl+a`. Check:
- System keyboard shortcuts
- Other terminal multiplexers (tmux/screen)

### Status Bar Not Updating
The status bar updates every second. If not visible:
- Check `enable_tab_bar = true`
- Verify `hide_tab_bar_if_only_one_tab = false`

## Development Workspace

### Automated Project Setup
Use the `dev-workspace` command for instant project environment:

```bash
# Launch in current directory
dev-workspace

# Launch for specific project
dev-workspace my-project
```

**Creates 4-pane layout:**
```
┌─────────────┬─────────────┐
│   Terminal  │    helix    │
│  (focused)  │  (editor)   │
├─────────────┼─────────────┤
│   lazygit   │    btop     │
│    (git)    │  (monitor)  │
└─────────────┴─────────────┘
```

### Quick Development Layout
The `Leader + w` keybinding creates the original 4-tile layout:
- **Top-left**: Terminal (main workspace)
- **Top-right**: btop (system monitoring)
- **Bottom-left**: lazygit (git operations)
- **Bottom-right**: Free terminal

### Smart Project Detection
The `dev-workspace` script automatically detects project types:
- **Node.js**: Suggests `npm run dev`
- **Rust**: Suggests `cargo watch -x run`
- **Docker**: Suggests `docker-compose up`
- **Makefile**: Suggests `make dev`

## Prompt Configuration

This setup uses **Starship** as the primary prompt for maximum performance and modernization.

### Current Setup
- **Default**: Starship (50ms faster rendering than Powerlevel10k)
- **Configuration**: `~/.config/starship.toml` (managed by chezmoi)
- **Features**: Two-line layout, git integration, command duration, context awareness

### Customizing Starship
```bash
# Edit configuration
chezmoi edit ~/.config/starship.toml

# Common customizations
[directory]
style = "32 bold"  # Change directory color to green

[git_branch]
symbol = "🌱 "     # Custom git branch symbol

# Apply changes
chezmoi diff && chezmoi apply
```

### Legacy Prompt Support
Powerlevel10k remains available for compatibility:
```bash
# Temporarily switch to P10k (not recommended)
export PROMPT_THEME="p10k"
exec zsh
```

## Shell Setup (Zsh + Prezto)

This setup uses **Zsh** with the **Prezto** framework in a complementary architecture with Starship.

### Architecture Philosophy
- **Prezto**: Provides shell enhancements (syntax highlighting, completions, history)
- **Starship**: Handles prompt rendering (excluded Prezto's prompt module)
- **Result**: Best of both worlds - rich shell features + blazing fast prompt

### Prezto Modules (Optimized)
Our configuration loads these modules in `.zpreztorc`:
```bash
'environment'              # Environment variable management
'terminal'                 # Auto-titles for tabs/windows  
'editor'                   # Emacs key bindings
'history'                  # Enhanced history management
'directory'                # Directory navigation enhancements
'spectrum'                 # Color support
'utility'                  # Safer file operations
'completion'               # Enhanced tab completions
'git'                      # Git integration and shortcuts
'python'                   # Python environment support
'osx'                      # macOS-specific utilities
'macports'                 # Package manager integration
'syntax-highlighting'      # Real-time command syntax validation
'history-substring-search' # Enhanced history navigation
# 'prompt' - EXCLUDED: Starship handles prompt rendering
```

### Key Features
- **Syntax Highlighting**: Commands turn green when valid, red when invalid
- **Auto-suggestions**: Fish-style command suggestions based on history
- **Smart Completions**: Context-aware tab completion
- **Auto-titling**: Terminal/tab titles update with current directory
- **Git Integration**: Enhanced git aliases and status display

## Philosophy

This configuration implements an **ultra-modern terminal-first development environment**:

### Core Principles
- **Performance First**: GPU acceleration, sub-200ms startup, 50ms prompt rendering
- **Aggressive Modernization**: Latest tools that push the boundaries of terminal capabilities
- **IDE-Rival Experience**: Complete development environment without leaving the terminal
- **Keyboard-Driven Workflow**: Every action accessible via leader keys and shortcuts
- **Versionable Configuration**: Every setting managed through chezmoi templates

### Design Goals
- **Minimize Context Switching**: File management, editing, git, docker, k8s all in terminal
- **Maximize Productivity**: One-key access to all development tools
- **Preserve Compatibility**: All muscle memory and existing workflows maintained
- **Enable Discoverability**: Visual indicators and smart defaults guide usage

### Modern Terminal Revolution
This setup demonstrates that in 2025, terminal environments can rival any IDE:
- Visual file management with image previews (yazi)
- LSP-powered editing with syntax highlighting (helix)
- Real-time system monitoring (btop, procs, bandwhich)
- Professional API development (atac)
- Enterprise container/k8s management (lazydocker, k9s)

All while being completely portable, lightweight, and blazingly fast.