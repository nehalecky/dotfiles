# dotfiles

Modern dotfiles management with [chezmoi](https://chezmoi.io/) and XDG Base Directory compliance.

> **Note**: This repository uses `$HOME` paths throughout. Replace any hardcoded paths with your home directory.

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[Project History](docs/PROJECT-HISTORY.md)** - All changes and learnings
- **[Secrets Management](docs/SECRETS-MANAGEMENT.md)** - 1Password integration & encryption
- **[Applications Guide](docs/APPLICATIONS.md)** - Detailed tool documentation
- **[Claude Instructions](docs/CLAUDE.md)** - AI assistant context

## 🚀 Quick Setup

### Prerequisites

Install [Homebrew](https://brew.sh/) if not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Initialize Dotfiles

```bash
# Install chezmoi and apply dotfiles
brew install chezmoi
chezmoi init --apply $GITHUB_USERNAME/dotfiles

# Install all dependencies (chezmoi will prompt about Brewfile updates)
brew bundle
```

> **Tip**: Chezmoi handles all dotfile management. Use `chezmoi update` to pull latest changes and `chezmoi apply` to apply them.

## 🔐 Secrets Management

This repository uses a **hybrid secrets strategy** with [1Password](https://1password.com/) as the canonical source:

- **Development**: Secrets pulled directly from 1Password
- **Restricted Environments**: Falls back to age-encrypted files
- **Automatic Detection**: Templates adapt based on environment

See [Secrets Management Guide](docs/SECRETS-MANAGEMENT.md) for full details.

## 📦 Dependency Management

All dependencies are managed via [Homebrew](https://brew.sh/) with a versioned `Brewfile`:

### What's Included
- **56 Command-line tools** - Modern replacements for Unix utilities
- **32 Desktop applications** - Development and productivity apps  
- **11 VS Code extensions** - Language and tool support

### Key Commands
```bash
# Install all dependencies
brew bundle

# Update dependencies
brew upgrade && brew upgrade --cask

# Clean up unused dependencies
brew bundle cleanup
```

See [Dependency Analysis](docs/homebrew-analysis.md) for detailed package information.

## 🛠 What's Managed

### Shell Environment
- **Shell**: [Zsh](https://www.zsh.org/) with [Prezto](https://github.com/sorin-ionescu/prezto)
- **Prompt**: [Powerlevel10k](https://github.com/romkatv/powerlevel10k) (planning to migrate to Starship)
- **Enhancements**: [bat](https://github.com/sharkdp/bat), [eza](https://github.com/eza-community/eza), [ripgrep](https://github.com/BurntSushi/ripgrep), [fzf](https://github.com/junegunn/fzf)

### Security & Authentication
- **Password Manager**: [1Password](https://1password.com/) with CLI integration
- **SSH**: 1Password SSH agent at `$HOME/.1password/agent.sock`
- **Git Signing**: GPG via [GPG Suite](https://gpgtools.org/)

### Development Tools
- **Version Control**: [Git](https://git-scm.com/) + [GitHub CLI](https://cli.github.com/)
- **Containers**: [Docker](https://www.docker.com/)
- **Python**: [uv](https://github.com/astral-sh/uv) package manager
- **Editors**: [VS Code](https://code.visualstudio.com/), [Cursor](https://cursor.sh/), [Emacs](https://www.gnu.org/software/emacs/)

## 🎯 Key Features

### XDG Compliance
- Configs organized under `$HOME/.config/`
- Cache in `$HOME/.cache/`
- Data in `$HOME/.local/share/`

### Security First
- No hardcoded secrets
- SSH keys never on disk
- Encrypted fallback for restricted environments

### Modern Terminal
- Fast, informative prompt
- Smart command replacements
- Powerful search and navigation

## 🔧 Common Workflows

### Update Everything
```bash
# Pull latest dotfiles and apply (auto-syncs Brewfile)
chezmoi update

# Update Homebrew packages
brew update && brew upgrade
```

> **Note**: Running `chezmoi apply` automatically checks if your Brewfile is out of sync with installed packages and prompts to update it.

### Check What Changed
```bash
# See pending changes
chezmoi diff

# See managed files status
chezmoi status
```

### Add New Configurations
```bash
# Add a new config file
chezmoi add ~/.config/newapp/config

# Add with encryption
chezmoi add --encrypt ~/.config/sensitive/config
```

### Customization

1. **Fork** this repository
2. **Modify** configurations as needed
3. **Test** with `chezmoi diff`
4. **Apply** with `chezmoi apply`

## 🆘 Troubleshooting

### Common Issues

**Chezmoi not found**
```bash
brew install chezmoi
```

**1Password CLI issues**
```bash
# Sign in
eval $(op signin)

# Verify
op vault list
```

**Missing dependencies**
```bash
brew bundle check
brew bundle install
```

### Getting Help
- Chezmoi: `chezmoi doctor`
- Homebrew: `brew doctor`
- This repo: Check [Project History](docs/PROJECT-HISTORY.md)

## 📖 References

- [Chezmoi Documentation](https://www.chezmoi.io/)
- [Homebrew Documentation](https://docs.brew.sh/)
- [1Password CLI](https://developer.1password.com/docs/cli/)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

---

*Managed with [chezmoi](https://chezmoi.io/) • Secured by [1Password](https://1password.com/) • Powered by [Homebrew](https://brew.sh/)*