# Modern Development Environment Dotfiles

*Chezmoi-managed dotfiles for ultra-modern terminal-first development*

> **📖 [Complete Documentation](https://nehalecky.github.io/dotfiles/)** | **⚡ Quick Setup Below**

## Overview

A comprehensive development environment built around modern terminal-first tools, managed with [chezmoi](https://chezmoi.io) for consistent deployment across machines. Features AI-enhanced development with Claude Code integration and 67+ performance-optimized tools.

## Quick Setup

**⏱️ 5 minutes to full development environment**

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles (includes all 67+ tools)
brew install chezmoi && chezmoi init --apply https://github.com/nehalecky/dotfiles.git
```

**What You Get:**
- **GPU-Accelerated Terminal** - WezTerm with 120fps rendering
- **Modern Tool Suite** - 67+ performance-optimized CLI tools
- **AI Development** - Claude Code with 14 specialized agents
- **Clean Configuration** - Hidden dotfiles following best practices

## Key Components

### Core Stack
- **Terminal**: WezTerm (GPU-accelerated, multiplexed)
- **Shell**: Zsh + Starship (fast, informative prompt)
- **Editor**: Helix/Emacs with LSP integration
- **Package Management**: Homebrew + uv (Python)

### Modern Replacements
| Traditional | Modern Alternative | Key Benefit |
|-------------|-------------------|-------------|
| `ls` | `eza` | Git integration, tree view |
| `cat` | `bat` | Syntax highlighting |
| `find` | `fd` | Faster, respects .gitignore |
| `grep` | `ripgrep` | 10x faster searches |
| `top` | `btop` | Beautiful system monitor |

### Claude Code Integration

Comprehensive [Claude Code](https://claude.ai/code) configuration with specialized agents:

- **14 Specialized Agents** - Development, consulting, research, platform operations
- **Memory Systems** - Project-specific context and methodologies
- **Workflow Automation** - Python hooks and custom commands
- **MCP Integrations** - GitHub, Google Workspace, Atlassian APIs

## Documentation

**📖 [Full Documentation Site](https://nehalecky.github.io/dotfiles/)**

**Quick References:**
- **[Getting Started](https://nehalecky.github.io/dotfiles/core/terminal-guide.html)** - Complete setup guide
- **[Development Practices](https://nehalecky.github.io/dotfiles/core/development-practices.html)** - Workflows and methodologies
- **[Claude Code Agents](https://nehalecky.github.io/dotfiles/claude/agent-guide.html)** - AI development integration
- **[System Architecture](https://nehalecky.github.io/dotfiles/architecture/system-overview.html)** - Technical deep dive

## Philosophy

**Terminal-First Development:**
- Single interface for all development tasks
- Sub-100ms tool launch times
- Consistent vim-inspired navigation
- Reproducible environments via code

**Dotfiles Best Practices:**
- Hidden configuration files (`~/.config`, `~/.local`)
- Chezmoi management for cross-machine deployment
- Secret integration with 1Password
- Clean `$HOME` directory

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

**Repository**: [nehalecky/dotfiles](https://github.com/nehalecky/dotfiles) • **Documentation**: [nehalecky.github.io/dotfiles](https://nehalecky.github.io/dotfiles/) • **License**: MIT