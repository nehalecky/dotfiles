# Dotfiles Architecture

## 🌐 100K' View

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
│   └── shell/                  # Shell environment
│       └── xdg-env.sh          # XDG variables
│
├── .local/                     # XDG Data
│   ├── share/
│   │   ├── chezmoi/            # Dotfiles repository
│   │   │   ├── README.md       # Main documentation
│   │   │   ├── Brewfile        # Dependency manifest
│   │   │   ├── docs/           # Documentation
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
└── .1password/                 # 1Password agent socket
    └── agent.sock
```

### Workflow Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     Interactive Layer                        │
│                  ┌─────────────────┐                        │
│                  │  dotfiles-tool  │                        │
│                  │   (main CLI)    │                        │
│                  └────────┬────────┘                        │
│                          │                                  │
├──────────────────────────┼──────────────────────────────────┤
│                          ▼                                  │
│                   Workflow Layer                            │
│  ┌──────────┬──────────┬──────────┬──────────┐           │
│  │  Setup   │  Update  │  Sync    │  Debug   │           │
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