# My Dots

*One command deploys a complete, AI-augmented development environment — personal or work profile, any Mac. Versioned Claude agents, memories, and skills follow you across machines and across interfaces: the same configuration powers both Claude Code in the terminal and Claude on the web.*

> **[Documentation](dot_docs/README.md)** | **[Setup Guide](SETUP.md)**

## Why

Every developer has set up a new machine from scratch. You install Homebrew, then your editor, then your shell plugins, then your git config, then the CLI tools you forgot you depended on. Two days later you realize you still don't have delta configured and your commit signing is broken. Six months later, you do it again on a work laptop and remember none of the steps.

Your development environment is software. It deserves version control, documentation, and reproducible builds — the same discipline you apply to production code.

This repository treats that idea seriously. [Chezmoi](https://chezmoi.io) manages every configuration file. A single `chezmoi init` on a fresh machine prompts for a profile — personal or work — then injects the correct git identity, SSH keys, 1Password items, Brewfile packages, and terminal theme. One repo, two machines, zero manual steps.

The environment is terminal-first, not out of nostalgia, but because terminals compose. Pipes chain tools together. SSH gives you the same interface on a remote server. Muscle memory transfers across machines. Sub-second launch times compound into hours saved over a year.

Claude Code is not bolted on as an afterthought. Twelve specialized agents, a persistent memory system, workflow automation hooks, and MCP integrations ship as versioned configuration alongside the shell and editor. Because the agents and memories live in the dotfiles repo, they deploy to every machine automatically — and the same configuration works whether you are in Claude Code at the terminal or Claude on the web. Your AI workflow is as reproducible as your shell config.

## Quick Setup

Fork this repository first, then:

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles
brew install chezmoi
chezmoi init --apply <your-github-username>
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
- **Memory system** storing project context and methodologies across sessions
- **Workflow automation** through Python hooks and custom commands
- **MCP integrations** connecting GitHub, Google Workspace, and Atlassian
- **Superpowers plugin** adding structured TDD, planning, and execution skills

Agents, memories, and skills are version-controlled alongside the rest of the dotfiles. Deploy to a new machine with `chezmoi apply` and your full AI configuration — context, behavior, and tooling — arrives with it. The same files power both Claude Code in the terminal and Claude on the web.

*Claude Code setup based on [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).*

## Documentation

- **[Documentation Index](dot_docs/README.md)** — Full reference for tools, architecture, and troubleshooting
- **[SETUP.md](SETUP.md)** — First-time installation, profile selection, and customization
- **[CLAUDE.md](CLAUDE.md)** — Claude Code configuration and [Superpowers](https://github.com/obra/superpowers) integration

## Technology Stack

- **Dotfiles Management**: chezmoi
- **Terminal**: WezTerm + tmux/zellij
- **Shell**: Zsh + Prezto + Starship
- **Package Managers**: Homebrew (macOS), uv (Python)
- **AI Integration**: Claude Code + specialized agents
- **Documentation**: GitHub Pages (auto-deployed)

## Contributing

This is a personal dotfiles repository built for my workflow. Explore and borrow freely, but expect opinionated defaults.

For questions or discussion, [open an issue](https://github.com/<your-github-username>/dotfiles/issues).

---

**Repository**: [dotfiles](https://github.com/<your-github-username>/dotfiles) | **Documentation**: [dot_docs/README.md](dot_docs/README.md) | **License**: MIT
