# Development Environment Dotfiles

*Chezmoi-managed dotfiles for terminal-first development*

> **[Documentation](dot_docs/README.md)** | **Quick Setup Below**

## Overview

Development environment built around terminal-first tools, managed with [chezmoi](https://chezmoi.io) for consistent deployment across machines. Features Claude Code integration with 19 specialized agents and 67+ command-line tools.

## Quick Setup

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles
brew install chezmoi && chezmoi init --apply https://github.com/nehalecky/dotfiles.git
```

This installs WezTerm with GPU acceleration, 67+ command-line tools, Claude Code with 19 specialized agents, and XDG-compliant dotfile organization.

## Key Components

### Core Stack
- **Terminal**: WezTerm (GPU-accelerated, multiplexed)
- **Shell**: Zsh + Starship prompt
- **Editor**: Helix/Emacs with LSP integration
- **Package Management**: Homebrew + uv (Python)

### Tool Suite
| Traditional | Replacement | Key Benefit |
|-------------|------------|-------------|
| `ls` | `eza` | Git integration, tree view |
| `cat` | `bat` | Syntax highlighting |
| `find` | `fd` | Faster, respects .gitignore |
| `grep` | `ripgrep` | Faster searches |
| `top` | `btop` | Interactive system monitor |

### Claude Code Integration

[Claude Code](https://claude.ai/code) configuration with specialized agents and workflow automation:

- **19 specialized agents** for development, research, and operations
- **Memory systems** for project context and methodologies
- **Workflow automation** via Python hooks and custom commands
- **MCP integrations** for GitHub, Google Workspace, Atlassian APIs
- **Superpowers plugin** for enhanced capabilities (October 2024)

Recent consolidation improved token efficiency by 42% (818 lines, ~65K tokens saved) through unified agent architecture.

*Initial Claude Code setup based on [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).*

## Documentation

**[Full Documentation](dot_docs/README.md)**

**Quick References:**
- **[Getting Started](dot_docs/core/terminal-guide.md)** - Setup guide
- **[Development Practices](dot_docs/core/development-practices.md)** - Workflows and methodologies
- **[Daily Workflows](dot_docs/core/workflows.md)** - Common task guides
- **[System Architecture](dot_docs/architecture/system-overview.md)** - Technical details

## Philosophy

**Terminal-First Development:**
- Consistent interface for development tasks
- Fast tool launch times
- Vim-inspired navigation patterns
- Reproducible environments via code

**Dotfiles Organization:**
- XDG-compliant configuration (`~/.config`, `~/.local`)
- Chezmoi management for cross-machine deployment
- Secret integration with 1Password
- Organized home directory structure

## Technology Stack

- **Dotfiles Management**: chezmoi
- **Terminal**: WezTerm + tmux/zellij
- **Shell**: Zsh + Prezto + Starship
- **Package Managers**: Homebrew (macOS), uv (Python)
- **AI Integration**: Claude Code + specialized agents
- **Documentation**: GitHub Pages (auto-deployed)

## Contributing

This is a personal dotfiles repository optimized for my development workflow. While you're welcome to explore and learn from the configuration, it's designed specifically for my setup and preferences.

For questions or discussions about the approaches used, feel free to [open an issue](https://github.com/nehalecky/dotfiles/issues).

---

**Repository**: [nehalecky/dotfiles](https://github.com/nehalecky/dotfiles) • **Documentation**: [dot_docs/README.md](dot_docs/README.md) • **License**: MIT
