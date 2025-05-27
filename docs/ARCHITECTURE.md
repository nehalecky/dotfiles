# Dotfiles Architecture

## 🌐 100K' View

```mermaid
graph TB
    subgraph "User's System"
        CM[chezmoi<br/>manager] --> DF[dotfiles<br/>repo]
        DF --> OP[1Password<br/>secrets]
        CM --> HOME[$HOME<br/>configs]
        DF --> HB[Homebrew<br/>deps]
        DF --> AGE[Age<br/>fallback]
    end
    
    style CM fill:#e8f4f8,stroke:#2e86de
    style DF fill:#f0f9ff,stroke:#0ea5e9
    style OP fill:#fff4e6,stroke:#f97316
    style HOME fill:#f0fdf4,stroke:#22c55e
    style HB fill:#fef3c7,stroke:#f59e0b
    style AGE fill:#fef2f2,stroke:#ef4444
```

**Text Alternative:**
```
┌─────────────────────────────────────────────────────────────┐
│                        User's System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   chezmoi   │───▶│   dotfiles   │───▶│  1Password   │  │
│  │  (manager)  │    │    (repo)    │    │  (secrets)   │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                    │          │
│         ▼                   ▼                    ▼          │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │    $HOME    │    │   Homebrew   │    │     Age      │  │
│  │   configs   │    │   (deps)     │    │  (fallback)  │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Detailed Architecture

### Core Systems

```
┌──────────────────────────────────────────────────────────────────┐
│                         Dotfiles Repository                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Source Control           Configuration          Documentation   │
│  ┌─────────────┐         ┌─────────────┐       ┌─────────────┐ │
│  │   GitHub    │         │  Templates  │       │    docs/    │ │
│  │  nehalecky/ │◀───────▶│   (.tmpl)   │       │  *.md files │ │
│  │  dotfiles   │         └─────────────┘       └─────────────┘ │
│  └─────────────┘                │                               │
│         ▲                       │                               │
│         │                       ▼                               │
│  ┌─────────────┐         ┌─────────────┐       ┌─────────────┐ │
│  │   chezmoi   │────────▶│    Hooks    │       │   Scripts   │ │
│  │   manage    │         │  (install)  │       │ (workflow)  │ │
│  └─────────────┘         └─────────────┘       └─────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                          Local System                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  XDG Directories          Home Files           Package Manager   │
│  ┌─────────────┐         ┌─────────────┐       ┌─────────────┐ │
│  │  ~/.config  │         │   ~/.zshrc  │       │  Homebrew   │ │
│  │  ~/.cache   │         │   ~/.ssh    │       │  /opt/brew  │ │
│  │  ~/.local   │         │   README.md │       │  Brewfile   │ │
│  └─────────────┘         └─────────────┘       └─────────────┘ │
│         │                       │                       │        │
│         └───────────────────────┴───────────────────────┘        │
│                                 │                                │
│                                 ▼                                │
│                         ┌─────────────┐                         │
│                         │   Secrets   │                         │
│                         │  Management │                         │
│                         └─────────────┘                         │
│                                 │                                │
│                ┌────────────────┴────────────────┐              │
│                ▼                                 ▼              │
│         ┌─────────────┐                  ┌─────────────┐       │
│         │  1Password  │                  │     Age     │       │
│         │   (live)    │                  │ (encrypted) │       │
│         └─────────────┘                  └─────────────┘       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
$HOME/
├── .config/                    # XDG Config (managed by chezmoi)
│   ├── git/                    # Git configuration
│   ├── npm/                    # NPM config
│   ├── docker/                 # Docker config
│   ├── chezmoi/                # Chezmoi config
│   │   └── chezmoi.toml        # Chezmoi settings
│   ├── op/                     # 1Password CLI
│   ├── iterm2/                 # Terminal config
│   ├── starship.toml           # Starship prompt config
│   └── shell/                  # Shell environment
│       └── xdg-env.sh          # XDG variables
│
├── .local/                     # XDG Data
│   ├── share/
│   │   ├── chezmoi/            # Dotfiles repository
│   │   │   ├── README.md       # Main documentation
│   │   │   ├── CLAUDE.md       # AI assistant context
│   │   │   ├── Brewfile        # Dependency manifest
│   │   │   ├── docs/           # Documentation
│   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   ├── TERMINAL-SETUP.md
│   │   │   │   └── archive/    # Historical docs
│   │   │   ├── scripts/        # Automation scripts
│   │   │   ├── .secrets/       # Encrypted secrets
│   │   │   └── *.tmpl          # Template files
│   │   └── gnupg/              # GPG keys
│   └── bin/                    # User scripts
│
├── .cache/                     # XDG Cache
│   ├── pip/                    # Python packages
│   └── yarn/                   # Node packages
│
├── .ssh/                       # SSH (must stay in $HOME)
├── .zshrc                      # Shell config (sourced by zsh)
├── .gitconfig                  # Git config (minimal, uses includes)
├── .wezterm.lua                # WezTerm terminal config
├── .p10k.zsh                   # Powerlevel10k prompt config
├── README.md                   # Repository documentation
├── CLAUDE.md                   # AI assistant context
├── .docs/                      # Symlink to ~/.local/share/chezmoi/docs
└── .1password/                 # 1Password agent socket
    └── agent.sock
```

### Workflow Layers

```mermaid
graph TD
    subgraph "User Interaction"
        USER[User] --> CM[chezmoi CLI]
        USER --> GIT[git commands]
    end
    
    subgraph "Management Layer"
        CM --> APPLY[chezmoi apply]
        CM --> EDIT[chezmoi edit]
        CM --> ADD[chezmoi add]
        GIT --> COMMIT[Commit & Push]
    end
    
    subgraph "Automation Layer"
        APPLY --> HOOKS[Chezmoi Hooks]
        HOOKS --> BREW[Brewfile Sync]
        HOOKS --> ITERM[iTerm2 Profiles]
    end
    
    style USER fill:#e0e7ff,stroke:#6366f1
    style CM fill:#dbeafe,stroke:#3b82f6
    style HOOKS fill:#fef3c7,stroke:#f59e0b
```

**Text Alternative:**
```
┌─────────────────────────────────────────────────────────────┐
│                     Interactive Layer                        │
│                  ┌─────────────────┐                        │
│                  │   chezmoi CLI   │                        │
│                  │  (direct use)   │                        │
│                  └────────┬────────┘                        │
│                          │                                  │
├──────────────────────────┼──────────────────────────────────┤
│                          ▼                                  │
│                   Workflow Layer                            │
│  ┌──────────┬──────────┬──────────┬──────────┐           │
│  │  Apply   │  Edit    │  Add     │  Diff    │           │
│  │  System  │  Deps    │  Secrets │  Issues  │           │
│  └──────────┴──────────┴──────────┴──────────┘           │
│                          │                                  │
├──────────────────────────┼──────────────────────────────────┤
│                          ▼                                  │
│                    Tool Layer                               │
│  ┌──────────┬──────────┬──────────┬──────────┐           │
│  │ chezmoi  │Homebrew  │1Password │   Age    │           │
│  │ manage   │ bundle   │   CLI    │ encrypt  │           │
│  └──────────┴──────────┴──────────┴──────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Key Workflows

### Initial Setup
```
User ──▶ Install Homebrew ──▶ Install chezmoi ──▶ chezmoi init
                                      │
                                      ▼
                              Run install hooks
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
            Install 1Password CLI              Apply dotfiles
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      ▼
                                 brew bundle
```

### Secret Management
```
Development Environment                    Restricted Environment
         │                                          │
         ▼                                          ▼
Check for 'op' command ─────────┐       No 'op' command found
         │                      │                   │
         ▼                      │                   ▼
Pull from 1Password             │         Use .secrets/*.age files
         │                      │                   │
         └──────────────────────┴───────────────────┘
                                │
                                ▼
                        Render templates
```

### Update Workflow
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Check     │────▶│   Update    │────▶│    Test     │
│  Updates    │     │  Packages   │     │   Changes   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
   chezmoi           brew upgrade         chezmoi diff
   update            brew bundle          chezmoi apply
```

## 🎯 Design Principles

1. **Single Source of Truth**
   - Dotfiles: GitHub repository
   - Secrets: 1Password
   - Dependencies: Brewfile

2. **Environment Flexibility**
   - Works with/without 1Password
   - Adapts to system capabilities
   - Graceful fallbacks

3. **Security First**
   - No plaintext secrets
   - SSH keys in 1Password
   - Encrypted backups

4. **Automation**
   - Hooks for setup
   - Scripts for workflows
   - Unified CLI tool

5. **Documentation**
   - Self-documenting code
   - Comprehensive guides
   - Historical tracking