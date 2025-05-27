# Legacy Setup Notes

This document preserves valuable setup instructions from the original dotfiles bare repo README.

## GPG Key Setup with Keybase

Following [this guide](https://gist.github.com/webframp/75c680930b6b2caba9a1be6ec23477c1) for signing git commits with keybase.io GPG key:

```bash
keybase pgp export | gpg --import
keybase pgp export --secret | gpg --allow-secret-key --import
gpg --list-secret-keys --keyid-format LONG
gpg --edit-key <GPG_KEY>
```

In the GPG REPL, execute `trust` command:
```
gpg> trust
Your decision? 5  # Ultimate trust
Do you really want to set this key to ultimate trust? (y/N) y
gpg> exit
```

## iTerm2 Terminal Setup

### Install iTerm2 and Fonts
```bash
brew install --cask iterm2 homebrew/cask-fonts/font-awesome-terminal-fonts
```

### Shell Integration
Enable [iTerm2 shell integration](https://www.iterm2.com/documentation-shell-integration.html):
```bash
curl -L https://iterm2.com/shell_integration/install_shell_integration.sh | bash
```

### Terminal Colors
Install [iTerm2 color Schemes](https://iterm2colorschemes.com):
```bash
# Clone repo
git clone git@github.com:mbadolato/iTerm2-Color-Schemes.git ~/repos/iTerm2-Color-Schemes

# Install all schemes
~/repos/iTerm2-Color-Schemes/tools/import-scheme.sh ~/repos/iTerm2-Color-Schemes/schemes/*
```

Select **Hardcore** color scheme:
- Preferences > Profile > Colors > Color Preferences (dropdown) > Hardcore

### Font Configuration
In iTerm Preferences > Profile > Text:
- ✓ Use built-in Powerline glyphs
- Font: **Inconsolata Awesome** (Fixed Width)
- ✓ Use ligatures
- ✓ Anti-aliased
- Font size: 14 or 15

## Dotfiles Bare Repo Usage (Legacy Method)

**Note**: We now use chezmoi, but this documents the previous bare repo approach.

### Initial Setup
```bash
export DOTFILES_CONFIG_PATH=$HOME/.dotfiles-config
git init --bare $DOTFILES_CONFIG_PATH
alias dotfiles='git --git-dir=$DOTFILES_CONFIG_PATH --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
dotfiles remote add origin git@github.com:nehalecky/dotfiles-config.git
```

### Replication on New Machine
```bash
git clone --bare git@github.com:nehalecky/.dotfiles-config.git $HOME/.dotfiles-config
alias dotfiles='git --git-dir=$HOME/.dotfiles-config/ --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
dotfiles checkout
```

### Daily Usage
```bash
dotfiles status
dotfiles add .gitignore
dotfiles commit -m 'Add gitignore'
dotfiles push
```

## Legacy Keybase SSH Symlink

**Note**: Now using 1Password SSH agent instead.

Previously used Keybase for SSH key storage:
```bash
sudo ln -s /Volumes/Keybase/private/nehalecky/.ssh/ ~/.ssh
ssh-add ~/.ssh/id_ed25519
```

## Additional Terminal Tools

Enhanced Unix utilities that were recommended:
- `exa` → Now using `eza` (actively maintained fork)
- `ripgrep` (`rg`) - Fast grep replacement
- `bat` - Better cat with syntax highlighting
- `tealdeer` (`tldr`) - Simplified man pages
- `fzf` - Fuzzy finder
- `htop` → Now using `btop` (more modern)