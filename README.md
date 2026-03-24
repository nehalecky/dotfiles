# My Dots

*One command deploys a complete, AI-augmented development environment — personal or work profile, any Mac. Versioned Claude agents, memories, and skills follow you across machines and across interfaces: the same configuration powers both Claude Code in the terminal and Claude on the web.*

> **[Documentation](dot_docs/README.md)** | **[Setup Guide](SETUP.md)**

## Why

Your development environment is software. It deserves version control, documentation, and reproducible builds — the same discipline you apply to production code. [Chezmoi](https://chezmoi.io) manages every configuration file here; a single `chezmoi init` on a fresh machine prompts for a profile — personal or work — then wires up the correct git identity, SSH keys, Brewfile packages, and terminal theme automatically. Twelve specialized Claude Code agents, a persistent memory system, and workflow hooks ship as versioned configuration alongside the shell and editor, so the same AI workflow reproduces on every machine as reliably as the shell config does.

## Quick Setup

> **Fork this repo first.** `chezmoi init` pulls from your own fork so your identity, keys, and profile choices stay private. See [SETUP.md](SETUP.md) for the full walkthrough.

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles from your fork
brew install chezmoi
chezmoi init --apply <your-github-username>
```

`chezmoi init` prompts for your profile (personal/work), git identity, SSH keys, and terminal emulator (WezTerm, iTerm2, Ghostty, and others supported). It installs only the packages and configs for your choices — faster and friendlier developer tools, 12 Claude Code agents, and XDG-compliant dotfile organization.

## Key Components

### Core Stack
- **Terminal**: WezTerm, iTerm2, Ghostty, Kitty, or Alacritty (chosen at init)
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
- **Voice notifications** announcing task completion and input prompts, powered by local neural TTS (Kokoro) with ElevenLabs and OpenAI as optional cloud upgrades

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
