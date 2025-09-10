# Documentation Index

*Ultra-modern terminal-first development environment documentation*

## 🏗️ Quick Install

**Deploy complete environment from bare macOS:**

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install chezmoi and deploy dotfiles (includes all 67+ tools)
brew install chezmoi && chezmoi init --apply https://github.com/nehalecky/dotfiles.git
```

This approach uses chezmoi's native bootstrap system with embedded scripts to install all packages and configure your complete development environment.

## 🚀 Getting Started

**New to the system?** Start here for immediate productivity:

- **[Terminal Guide](core/terminal-guide.md)** - Complete terminal-first development environment guide
- **[Development Practices](core/development-practices.md)** - Standards, workflows, and modern patterns
- **[Daily Workflows](core/workflows.md)** - Step-by-step guides for common tasks
- **[Commands & Shortcuts](core/shortcuts.md)** - Complete reference for all commands and shortcuts

## 🧠 AI Development Integration

**Claude Code & AI-Assisted Development:**

- **[Claude Memory System](claude/memory-system.md)** - Modular AI context management and smart project templates
- **[Claude Code Trust Setup](claude/trust-setup.md)** - Security configuration for AI development
- **[Claude Code Emacs Guide](claude/emacs-integration.md)** - Advanced editor integration
- **[VS Code Claude Integration](claude/vscode-integration.md)** - VS Code AI workflow setup

## 🔧 System Architecture & Configuration

**Deep technical guides for system understanding:**

- **[Architecture](architecture/system-overview.md)** - System design and visual diagrams
- **[Secrets Management](architecture/secrets-management.md)** - 1Password + SSH authentication strategy
- **[Python Development](architecture/python-development.md)** - Modern Python workflow with uv
- **[Applications Guide](architecture/applications.md)** - Complete catalog of all 67+ installed tools

## 📖 Reference & History

**Specialized guides and historical context:**

- **[Commands & Shortcuts](core/shortcuts.md)** - Complete command and shortcut reference
- **[Important Instruction Reminders](reference/reminders.md)** - Key development principles

## 📚 Documentation Philosophy

### Structure
- **Getting Started** - Immediate productivity guides for new users
- **AI Development Integration** - Claude Code modular memory system and AI workflows
- **System Architecture** - Deep technical guides for system understanding
- **Reference & History** - Commands, shortcuts, and evolutionary context

### Principles
1. **Practical First** - Focus on daily workflows and real usage patterns
2. **AI-Enhanced Development** - Document the Claude Code modular memory approach
3. **Terminal-First** - Ultra-modern TUI tools as the primary development interface
4. **Integration Focus** - Show how tools work together, not in isolation
5. **Modular Organization** - Documentation mirrors the modular memory system architecture

### Navigation Guide

**First Time Setup:** 
1. [Terminal Guide](core/terminal-guide.md) → [Daily Workflows](core/workflows.md)
2. [Claude Memory System](claude/memory-system.md) → [Development Practices](core/development-practices.md)

**Daily Development:**
- Quick reference: [Commands & Shortcuts](core/shortcuts.md)
- AI context: [Claude Memory System](claude/memory-system.md)
- Troubleshooting: [Daily Workflows](core/workflows.md#troubleshooting)

**System Administration:**
- Configuration: [Architecture](architecture/system-overview.md) + [Secrets Management](architecture/secrets-management.md)
- Tools: [Applications Guide](architecture/applications.md)

---

*Start with [Terminal Guide](core/terminal-guide.md) to transform your development workflow, then explore [Claude Memory System](claude/memory-system.md) for AI-enhanced development!*