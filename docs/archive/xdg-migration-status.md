# XDG Base Directory Migration Status

This tracks the migration of dotfiles to XDG-compliant locations.

## Already Migrated to ~/.config/
✅ claude - Claude AI configuration
✅ conda - Conda configuration (though conda is now removed)
✅ docker - Docker configuration
✅ git - Git configuration
✅ npm - NPM configuration
✅ ipython - IPython configuration
✅ jupyter - Jupyter configuration
✅ shell - Shell environment scripts (including xdg-env.sh)
✅ btop, htop - System monitoring tools
✅ op - 1Password CLI
✅ gh - GitHub CLI
✅ chezmoi - Dotfile manager
✅ iterm2 - Terminal configuration

## Recently Migrated (2025-05-23)
- [x] `~/.gnupg` → `~/.local/share/gnupg` (GPG keys and config)
- [x] `~/.gitignore` → `~/.config/git/ignore` (Global gitignore)
- [x] `~/.fzf.bash`, `~/.fzf.zsh` → `~/.config/fzf/` (FZF configs)
- [x] `~/.iterm2_shell_integration.zsh` → `~/.config/iterm2/shell_integration.zsh`
- [x] Removed `.bash_profile` (unused)
- [x] Created minimal `.bashrc` stub for compatibility

## Still to Migrate

### High Priority (Actively Used)
- [ ] `~/.ssh` → Keep in home (SSH requires this location)
- [ ] `~/.cursor` → `~/.config/cursor` (Cursor editor)
- [ ] `~/.vscode` → `~/.config/Code` (VS Code, check if supported)

### Medium Priority (Occasionally Used)
- [ ] `~/.matplotlib` → `~/.config/matplotlib`
- [ ] `~/.julia` → Check Julia's XDG support
- [ ] `~/.pixi` → `~/.config/pixi` (Python package manager)

### Low Priority (Legacy/Unused)
- [ ] `~/.atom` → Can be removed (deprecated editor)
- [ ] `~/.emacs.d` → Keep if using Emacs
- [ ] `~/.mono` → Legacy .NET runtime
- [ ] `~/.sonic-pi` → Music programming environment
- [ ] `~/.theano` → Legacy deep learning library

### Shell Files (Must Stay in Home)
✅ `.zshrc`, `.zshenv`, `.zprofile`, `.zlogin`, `.zlogout` - Zsh looks here
✅ `.zpreztorc` - Prezto configuration
✅ `.gitconfig` - Git stub with includes
✅ `.p10k.zsh` - Powerlevel10k prompt config

### System/Tool Files (Cannot Move)
✅ `.CFUserTextEncoding` - macOS system file
✅ `.zsh_history`, `.zhistory` - Shell history
✅ `.1password` - 1Password socket location
✅ `.ssh` - SSH requires this exact location

## Next Steps

1. **Migrate GnuPG** (most important):
   ```bash
   mkdir -p ~/.local/share/gnupg
   cp -r ~/.gnupg/* ~/.local/share/gnupg/
   export GNUPGHOME="$HOME/.local/share/gnupg"
   # Test GPG operations before removing old directory
   ```

2. **Update shell environment** - Ensure xdg-env.sh has all needed exports

3. **Clean up legacy directories** - Remove unused applications

4. **Document in chezmoi** - Ensure all XDG paths are managed