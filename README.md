# My Dots

*Chezmoi-managed dotfiles for terminal-first development*

> **[Documentation](dot_docs/README.md)** | **Quick Setup Below**

## Overview

Terminal-first development environment managed with [chezmoi](https://chezmoi.io) for consistent deployment across machines. Includes 12 Claude Code agents, 60+ command-line tools, and multi-profile support for personal and work machines.

## Quick Setup

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles
brew install chezmoi && chezmoi init --apply https://github.com/nehalecky/dotfiles.git
# Replace 'nehalecky' with your GitHub username if forking
```

This installs WezTerm with GPU acceleration, 60+ command-line tools, 12 Claude Code agents, and XDG-compliant dotfile organization.

See [SETUP.md](SETUP.md) for detailed first-time setup, profile selection (personal/work), and customization options.

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

- **12 agents** covering development, research, and operations
- **Memory system** storing project context and methodologies
- **Workflow automation** through Python hooks and custom commands
- **MCP integrations** connecting GitHub, Google Workspace, and Atlassian
- **Superpowers plugin** adding structured TDD, planning, and execution skills (October 2024)

*Claude Code setup based on [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).*

## Documentation

Full documentation for this environment:
- **[Documentation Index](dot_docs/README.md)** - Start here for setup, tools, and architecture

Key docs:
- [Setup Guide](dot_docs/setup-guide.md) - First-time installation and customization
- [Tool Reference](dot_docs/tool-reference.md) - All 60+ tools, commands, shortcuts
- [Architecture](dot_docs/architecture.md) - System design and decisions

For Claude Code configuration and [Superpowers](https://github.com/obra/superpowers) integration, see [CLAUDE.md](CLAUDE.md).

## Philosophy

**Terminal-First Development:**
- One interface for all development tasks
- Sub-second tool launch times
- Vim-inspired navigation throughout
- Reproducible environments defined in code

**Dotfiles Organization:**
- XDG-compliant layout (`~/.config`, `~/.local`)
- Chezmoi-managed cross-machine deployment
- 1Password integration for secrets
- Clean home directory structure

**Multi-Profile Support:** One repo serves both personal and work machines. `chezmoi init` prompts for a profile and injects the matching git identity, SSH keys, 1Password items, Brewfile packages, and terminal theme.

## Technology Stack

- **Dotfiles Management**: chezmoi
- **Terminal**: WezTerm + tmux/zellij
- **Shell**: Zsh + Prezto + Starship
- **Package Managers**: Homebrew (macOS), uv (Python)
- **AI Integration**: Claude Code + specialized agents
- **Documentation**: GitHub Pages (auto-deployed)

## Contributing

This is a personal dotfiles repository built for my workflow. Explore and borrow freely, but expect opinionated defaults.

For questions or discussion, [open an issue](https://github.com/nehalecky/dotfiles/issues).

---

**Repository**: [nehalecky/dotfiles](https://github.com/nehalecky/dotfiles) • **Documentation**: [dot_docs/README.md](dot_docs/README.md) • **License**: MIT
