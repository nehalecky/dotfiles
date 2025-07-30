# ⚡ Ultra-Modern Terminal Development Environment

*A terminal-first development setup that eliminates context switching and maximizes productivity*

**🚀 Performance**: Sub-200ms startup • 120fps rendering • Instant tool access  
**🔐 Security**: 1Password integration • SSH signing • Zero secrets on disk  
**🎯 Productivity**: Leader key system • Automated workspaces • 10+ integrated TUI tools

> Transform your development workflow from fragmented GUI apps to a unified terminal powerhouse

## 🎯 Why This Setup?

**The Problem**: Traditional development environments are fragmented across multiple apps, slow to start, and require constant context switching between terminal, file manager, git GUI, Docker Desktop, etc.

**The Solution**: A unified terminal-first environment where everything is accessible via a single leader key (`Ctrl+a`):

```bash
Ctrl+a f  →  📁 File manager (yazi) with image previews
Ctrl+a e  →  ✏️  Modern editor (helix) with built-in LSP
Ctrl+a g  →  🔄 Git interface (lazygit) - no more GUI apps
Ctrl+a d  →  🐳 Docker management (lazydocker) - bye Docker Desktop
Ctrl+a k  →  ☸️  Kubernetes (k9s) - cluster management in terminal
Ctrl+a a  →  🌐 API testing (atac) - Postman in your terminal
Ctrl+a w  →  🚀 Launch 4-pane development workspace instantly
```

**The Result**: 
- **10x faster** workflow switching between tools
- **Zero context switching** - everything in one interface
- **Blazing performance** - GPU-accelerated terminal, optimized prompt
- **Bulletproof security** - 1Password handles all authentication

## 🚀 Quick Setup

**⏱️ 5-minute setup to transform your terminal**

```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install and initialize dotfiles
brew install chezmoi
chezmoi init --apply nehalecky/dotfiles

# 3. Install all tools and apps (67+ packages)
brew bundle

# 4. Restart your terminal and press Ctrl+a f to explore!
```

**🎉 That's it!** Your terminal now has:
- **Instant access** to file manager, editor, git, docker, kubernetes
- **Leader key shortcuts** displayed on startup to help you learn
- **1Password integration** for secure authentication
- **Modern TUI tools** replacing slow GUI applications

## 🛠️ What's Included

### 🔥 Ultra-Modern Terminal Stack

**Terminal & Shell**
- [**WezTerm**](https://wezfurlong.org/wezterm/) - GPU-accelerated terminal with 120fps rendering
- [**Starship**](https://starship.rs/) - Blazing fast prompt (50ms faster than Powerlevel10k)
- [**Zsh + Prezto**](https://github.com/sorin-ionescu/prezto) - Advanced shell with intelligent completions

**Leader Key TUI Tools** (`Ctrl+a` + key)
- [**yazi**](https://github.com/sxyazi/yazi) `f` - File manager with image previews and modern navigation
- [**helix**](https://github.com/helix-editor/helix) `e` - Post-modern modal editor with built-in LSP
- [**lazygit**](https://github.com/jesseduffield/lazygit) `g` - Intuitive git interface (replace Git GUI apps)
- [**lazydocker**](https://github.com/jesseduffield/lazydocker) `d` - Container management (replace Docker Desktop)
- [**k9s**](https://github.com/derailed/k9s) `k` - Kubernetes cluster management and monitoring
- [**atac**](https://github.com/Julien-cpsn/ATAC) `a` - API client (replace Postman)
- [**procs**](https://github.com/dalance/procs) `p` - Modern process viewer (replace Activity Monitor)
- [**bandwhich**](https://github.com/imsnif/bandwhich) `n` - Network monitor by process
- [**dust**](https://github.com/bootandy/dust) `u` - Disk usage analyzer (replace Disk Utility)
- [**zellij**](https://github.com/zellij-org/zellij) `s` - Modern session manager

### 🔐 Security & Authentication

- [**1Password**](https://1password.com/) - SSH agent with Touch ID/Apple Watch authentication
- [**GitHub CLI**](https://cli.github.com/) - GitHub operations without keychain prompts
- **SSH Commit Signing** - All commits signed via 1Password (no GPG complexity)
- **Zero Secrets on Disk** - All credentials managed securely

### 📦 67+ Modern Development Tools

**Enhanced Unix Utilities**
- [**bat**](https://github.com/sharkdp/bat) - Better `cat` with syntax highlighting
- [**eza**](https://github.com/eza-community/eza) - Modern `ls` replacement
- [**ripgrep**](https://github.com/BurntSushi/ripgrep) - Ultra-fast search (replace `grep`)
- [**fzf**](https://github.com/junegunn/fzf) - Fuzzy finder for everything
- [**delta**](https://github.com/dandavison/delta) - Beautiful git diffs

**Development Stack**
- [**uv**](https://github.com/astral-sh/uv) - Blazing fast Python package manager
- **Node.js & npm** - JavaScript development
- [**chezmoi**](https://chezmoi.io/) - Dotfiles management across machines

## ⚡ Performance & Philosophy

### 🚀 Aggressive Performance Optimization
- **Sub-200ms shell startup** - Optimized Starship prompt and lazy loading
- **120fps terminal rendering** - WezTerm GPU acceleration for smooth experience  
- **Instant tool switching** - Leader key system eliminates menu navigation
- **Zero latency authentication** - 1Password biometric unlock (Touch ID/Apple Watch)

### 🧠 Terminal-First Philosophy
- **One Interface Rule All** - File management, editing, git, docker, kubernetes all in terminal
- **Keyboard-Driven Workflow** - Mouse usage minimized, everything accessible via shortcuts
- **Context Preservation** - No app switching means no mental context loss
- **Tool Integration** - Everything works together instead of isolated applications

### 🔒 Security Without Friction
- **1Password Integration** - All authentication through secure biometric unlock
- **SSH Signing** - Git commits signed via SSH (no GPG key management complexity)  
- **GitHub CLI Authentication** - No keychain prompts, secure token management
- **Zero Secrets on Disk** - All credentials managed by 1Password or encrypted storage

## 🔧 Daily Workflows  

### 🎮 Development Workspace Setup
```bash
# Launch 4-pane development workspace
Ctrl+a w
# Creates: main terminal, btop monitor, lazygit, and extra pane

# Or create project-specific workspace
dev-workspace my-project
# Auto-sets up project directory structure and tools
```

### ⚡ Instant Tool Access (Leader Key System)
```bash
Ctrl+a f    # 📁 Browse files with yazi (image previews, quick nav)
Ctrl+a e    # ✏️  Edit with helix (built-in LSP, no config needed)
Ctrl+a g    # 🔄 Git operations with lazygit (replace GUI apps)
Ctrl+a d    # 🐳 Docker management with lazydocker
Ctrl+a k    # ☸️  Kubernetes with k9s (real-time cluster monitoring)
Ctrl+a a    # 🌐 API testing with atac (terminal Postman)
Ctrl+a p    # 📊 Process monitoring with procs
Ctrl+a n    # 🌐 Network monitoring with bandwhich
```

### 🔄 Configuration Management (chezmoi)

**Quick Config Edit**
```bash
# Edit live config → sync to source → commit
vim ~/.zshrc
chezmoi add ~/.zshrc
chezmoi git -- commit -m "Update shell config"
```

**Safe Config Development**  
```bash
# Edit source → preview → apply → commit
chezmoi edit ~/.zshrc
chezmoi diff                    # Preview changes
chezmoi apply                   # Apply to home
chezmoi git -- commit -m "Update shell config"
```

**Sync Across Machines**
```bash
chezmoi update                  # Pull latest and apply
```

### 🔐 Secure Authentication Workflow
- **Git operations**: Handled automatically by GitHub CLI (no prompts)
- **SSH connections**: 1Password agent with Touch ID/Apple Watch
- **New repositories**: `gh repo create` integrates with chezmoi workflow

## 🆘 Quick Troubleshooting

```bash
# Leader key shortcuts not showing?
wezterm-shortcuts                   # Display shortcuts manually

# Tools not working?
brew bundle check                   # Check missing dependencies
brew bundle install                 # Install missing tools

# Authentication issues?
gh auth status                      # Check GitHub CLI auth
op signin                          # Sign in to 1Password

# Chezmoi sync issues?
chezmoi doctor                      # Diagnose chezmoi problems  
chezmoi status                      # Check file differences
```

## 📚 Documentation & Resources

### 📖 Detailed Guides
- **[CLAUDE.md](CLAUDE.md)** - AI assistant context and development guidelines
- **[Development Practices](docs/development-practices.md)** - Coding standards and workflows
- **[Architecture](docs/architecture.md)** - System design and structure
- **[Secrets Management](docs/secrets-management.md)** - 1Password integration details

### 🔗 External Resources
- [**Chezmoi Docs**](https://www.chezmoi.io/) - Dotfiles management
- [**WezTerm Guide**](https://wezfurlong.org/wezterm/) - Terminal configuration
- [**1Password CLI**](https://developer.1password.com/docs/cli/) - Authentication setup
- [**GitHub CLI**](https://cli.github.com/manual/) - Git operations

---

## 🚀 Ready to Transform Your Development Workflow?

```bash
brew install chezmoi && chezmoi init --apply nehalecky/dotfiles && brew bundle
```

*Experience the future of terminal-first development*

---
**Stack**: WezTerm • Starship • 1Password • GitHub CLI • 67+ Modern Tools  
**Philosophy**: Terminal-first • Security-focused • Performance-optimized