# myTUI - Terminal-First Development Environment

*Your personal terminal user interface for modern development*

## Mental Model

**One Terminal Rule All**: Instead of switching between Finder, GitHub Desktop, Docker Desktop, and dozens of other apps, myTUI brings everything into a single terminal interface with instant tool access via leader keys.

**Core Concepts:**
- **Leader Key System** (`Ctrl+a` + key) - Instant access to any tool without context switching
- **Workspace Automation** - Pre-configured 4-pane layouts for different project types
- **Configuration as Code** - All settings managed via chezmoi dotfiles system
- **HOME Integration** - Your home directory shows dotfiles git status in the prompt

## What You Get

### Terminal Stack
- **WezTerm** - GPU-accelerated terminal with 120fps rendering
- **Starship** - Fast, informative prompt with git integration
- **Zsh + Prezto** - Advanced shell with intelligent completions

### Tool Ecosystem  
- **File Management** - yazi with image previews and vim navigation
- **Code Editing** - helix with built-in LSP support
- **Git Operations** - lazygit for intuitive git workflows
- **Container Management** - lazydocker replacing Docker Desktop
- **API Testing** - atac as a terminal-based Postman alternative
- **Task Management** - taskwarrior-tui with custom color schemes
- **System Monitoring** - btop, bandwhich, dust for system insights

*See [complete tool reference →](docs/reference.md#tools)*

## Quick Setup

**⏱️ 5 minutes to terminal productivity**

```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Initialize dotfiles
brew install chezmoi
chezmoi init --apply nehalecky/dotfiles

# 3. Install all tools
brew bundle

# 4. Launch home workspace
workspace-home
```

**First Steps:**
1. Press `Ctrl+a f` to open the file manager
2. Press `Ctrl+a e` to open the editor  
3. Press `Ctrl+a g` to see git status
4. Press `Ctrl+a ?` to see all shortcuts

*For detailed setup and troubleshooting → [workflows guide](docs/workflows.md#installation)*

## Daily Usage

### Workspace Management
```bash
workspace-home          # Launch 4-pane home command center
workspace-dev myproject # Launch project-specific development workspace  
```

### Leader Key Shortcuts
Press `Ctrl+a` followed by:
- `f` - File manager (yazi)
- `e` - Editor (helix)  
- `g` - Git interface (lazygit)
- `d` - Docker management (lazydocker)
- `a` - API testing (atac)

*See [complete shortcuts reference →](docs/reference.md#shortcuts)*

### HOME Directory Magic
When in your home directory (`cd ~`), your prompt displays your dotfiles repository status:

```bash
░▒▓   ~   master ✘?⇡   12:52
#             ↑    ↑↑↑
#        branch  ││└── ahead of remote  
#                │└─── untracked files
#                └──── modified files
```

*Learn more about [configuration workflows →](docs/workflows.md#dotfile-management)*

## Where To Go Next

- **New to this setup?** Continue with [daily workflows →](docs/workflows.md)
- **Need a specific command?** Check the [reference guide →](docs/reference.md) 
- **Something not working?** See [troubleshooting →](docs/workflows.md#troubleshooting)
- **Want to customize?** Learn about [personalization →](docs/workflows.md#customization)

## Philosophy

**Terminal-First Development**: All development tools accessible from a single interface eliminates context switching, preserves mental state, and maximizes keyboard efficiency. Leader keys provide instant access at the speed of thought.

**Configuration as Code**: Every setting is versioned, reproducible, and shareable. Your entire development environment can be recreated on any machine with a single command.

---

**Stack**: WezTerm • Starship • chezmoi • 130+ Modern Tools  
**Approach**: Terminal-native • Security-focused • Performance-optimized