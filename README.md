# 🎮 myTUI

*Your personal terminal user interface*

**🚀 One Terminal**: All your dev tools in one place  
**⚡ Lightning Fast**: Sub-200ms startup, 120fps rendering  
**🔐 Fort Knox Security**: 1Password + SSH signing, zero secrets on disk  
**🎯 Zero Context Switching**: Leader key (`Ctrl+a`) → instant tool access

> Transform from app-hopping chaos to terminal zen 🧘‍♂️

## 🤔 Why myTUI?

**The Problem**: Development workflows are fragmented across multiple applications:
- Finder for files 
- GitHub Desktop for git
- Docker Desktop eating your RAM
- Postman for APIs
- Activity Monitor for debugging
- *Switch, switch, switch... context lost* 😵‍💫

**The myTUI Solution**: One terminal, leader key shortcuts, pure productivity:

```bash
Ctrl+a f  →  📁 yazi (file manager with image previews)
Ctrl+a e  →  ✏️  helix (editor with built-in LSP)  
Ctrl+a g  →  🔄 lazygit (git without the GUI)
Ctrl+a d  →  🐳 lazydocker (bye bye Docker Desktop)
Ctrl+a k  →  ☸️  k9s (Kubernetes in your terminal)
Ctrl+a a  →  🌐 atac (Postman? More like... not-man)
Ctrl+a w  →  🚀 4-pane dev workspace (instant productivity)
```

**The Result**: 
- **10x faster** workflow switching
- **Zero context loss** from app switching  
- **Your RAM is happy** (no more Electron apps)
- **Terminal street cred** 😎

## 🚀 Quick Setup

**⏱️ 5 minutes to terminal enlightenment**

```bash
# 1. Install Homebrew (if you're still living in the stone age)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Clone the magic
brew install chezmoi
chezmoi init --apply nehalecky/dotfiles

# 3. Install ALL the tools (130+ packages of pure joy)
brew bundle

# 4. Restart terminal, press Ctrl+a f, and prepare to be amazed 🤯
```

**🎉 That's it!** Your terminal now has shortcuts displayed on startup to help you learn.

## 🛠️ What You Get

### 🔥 Modern Terminal Stack
- **WezTerm** - GPU-accelerated, 120fps terminal 
- **Starship** - Blazing fast prompt (50ms faster than alternatives)
- **Zsh + Prezto** - Advanced shell with intelligent completions

### 🎮 Leader Key TUI Tools (`Ctrl+a` + key)
- **yazi** `f` - File manager with image previews and vim keys
- **helix** `e` - Post-modern editor with built-in LSP (no config needed!)
- **lazygit** `g` - Git interface that makes sense
- **lazydocker** `d` - Container management without the desktop bloat
- **k9s** `k` - Kubernetes cluster management
- **atac** `a` - API testing (terminal Postman)
- **procs** `p` - Modern process viewer 
- **btop** `m` - Beautiful system monitor
- **bandwhich** `n` - Network monitor by process
- **dust** `u` - Disk usage that doesn't suck
- **zellij** `s` - Session manager for pros

### 🔐 Security & Authentication  
- **1Password SSH Agent** - Touch ID/Apple Watch authentication
- **SSH Commit Signing** - All commits cryptographically signed
- **GitHub CLI Integration** - No more keychain prompts
- **Zero Secrets on Disk** - Everything handled securely

### 📦 130+ Modern Development Tools
**Enhanced Unix**: `bat`, `eza`, `ripgrep`, `fzf`, `delta`, `glow`  
**Development**: `uv` (Python), `node`, `gh`, `git`, `chezmoi`  
**TUI Everything**: File management, editing, git, docker, kubernetes, APIs  
**Apps**: Arc, Claude, Cursor, 1Password, Raycast, and more

## ⚡ Daily Workflow

### 🎮 Development Workspace Setup
```bash
Ctrl+a w    # Launch 4-pane workspace (main + btop + git + extra)
# Or for project-specific setup:
dev-workspace my-project
```

### 🔄 Configuration Management (chezmoi)
```bash
# Quick config edit → sync → commit  
vim ~/.zshrc && chezmoi add ~/.zshrc && chezmoi git -- commit -m "Update shell"

# Safe config development
chezmoi edit ~/.zshrc    # Edit source
chezmoi diff            # Preview changes  
chezmoi apply           # Apply to home
chezmoi git -- commit -m "Update shell config"

# Sync across machines
chezmoi update          # Pull latest + apply
```

### 🔐 Authentication Workflow
- **Git operations**: Automatic via GitHub CLI (no prompts!)
- **SSH connections**: 1Password agent with biometric unlock
- **New repos**: `gh repo create` integrates seamlessly

## 🆘 Getting Help

```bash
# Display shortcuts anytime
wezterm-shortcuts

# Check what's missing  
brew bundle check

# Diagnose issues
chezmoi doctor
gh auth status
op signin
```

## 🎯 Philosophy

### Why Terminal-First?
- **One Interface Rule All** - File management, editing, git, containers, kubernetes all in terminal
- **Keyboard > Mouse** - Your hands never leave the keyboard
- **Speed of Thought** - Tools appear instantly via leader key
- **Context Preservation** - No app switching = no mental context loss

### Why myTUI?
- **Personal** - Your customized terminal interface  
- **Approachable** - Fun learning curve, not intimidating
- **Integrated** - Tools work together, not in isolation
- **Powerful** - Professional capabilities with personality

## 📚 Documentation

- **[~/.docs/](file://$HOME/.docs/)** - Complete guides and references
- **[Modern Terminal Tools](file://$HOME/.docs/modern-terminal-tools.md)** - Usage guide for all TUI tools
- **[Development Practices](file://$HOME/.docs/development-practices.md)** - Workflows and patterns
- **[CLAUDE.md](CLAUDE.md)** - AI assistant context and guidelines

## 🚨 Troubleshooting

**Tools not working?**
```bash
brew bundle install    # Install missing tools
```

**Authentication issues?**
```bash
gh auth status         # Check GitHub CLI
op signin             # 1Password CLI
```

**Config sync issues?**
```bash
chezmoi status        # Check differences
chezmoi apply         # Apply pending changes
```

---

## 🎉 Welcome to myTUI!

*Where productivity meets personality in terminal form* 

**Ready to ditch the GUI life?** Start with `Ctrl+a f` and explore your new terminal universe! 🚀

---
**Stack**: WezTerm • Starship • 1Password • 130+ Modern Tools  
**Vibe**: Terminal-first • Security-focused • Performance-obsessed • Actually fun