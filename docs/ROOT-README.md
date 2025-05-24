# dotfiles

Modern dotfiles management with [chezmoi](https://chezmoi.io/) and XDG Base Directory compliance.

## 📚 Documentation

- **[Applications & Tools Guide](docs/APPLICATIONS.md)** - Detailed tool documentation
- **[Project History](docs/PROJECT-HISTORY.md)** - Changes and migration log
- **[Dependency Analysis](docs/homebrew-analysis.md)** - Homebrew package analysis
- **[Claude Instructions](docs/CLAUDE.md)** - AI assistant context
- **[Migration Notes](docs/conda-to-uv-migration.md)** - Python environment migration

## Quick Setup

```bash
# Install chezmoi and initialize dotfiles
brew install chezmoi
chezmoi init --apply nehalecky/dotfiles

# Install all dependencies
brew bundle
```

## What's Managed

### Configuration Files
- **Shell Environment**: Zsh with prezto framework and starship prompt
- **SSH Configuration**: 1Password SSH agent integration with dynamic key selection
- **Git Configuration**: User settings, aliases, and GPG signing
- **1Password**: SSH agent configuration at `~/.1password/agent.sock`
- **Terminal**: iTerm2 shell integration

### Dependencies (via Homebrew)

The `Brewfile` installs a curated set of tools organized by category:

- **56 Command-line tools** (formulae) - Enhanced Unix utilities, development tools
- **32 Desktop applications** (casks) - Editors, browsers, productivity apps
- **11 VS Code extensions** - Python, Markdown, and Jupyter support

📚 **See [Applications Guide](docs/APPLICATIONS.md) for detailed documentation** including:
- Complete tables with links and descriptions
- What each tool enhances or replaces  
- Installation categories and use cases
- Maintenance tips and philosophy

## Key Features

### 🔐 Security First
- SSH keys stored in 1Password, never on disk
- GPG signing for git commits
- SSH agent integration with key selection

### 🚀 Modern Terminal
- Starship prompt with git integration
- Enhanced commands (bat, eza, ripgrep)
- Fuzzy search for files and history

### 📦 Dependency Management
- All tools versioned in `Brewfile`
- Minimal dependencies (56 formulae, 32 casks)
- VS Code extensions included

### 🔄 Easy Maintenance
- Single command updates: `chezmoi update`
- Brew bundle for consistent environments
- Git-backed configuration history

## Architecture Notes

### Dependency Analysis
See [`docs/homebrew-analysis.md`](docs/homebrew-analysis.md) for a detailed breakdown of:
- Which packages are leaves vs dependencies
- What libraries are auto-installed
- Recommendations for package management

### Migration from Symlinks
This setup replaces a previous approach using:
- Bare git repo at `~/.dotfiles-config/`
- Symlinks to `.zprezto/runcoms/*`

Chezmoi now manages actual file content, eliminating symlink issues.

## Customization

1. **Fork this repository**
2. **Modify configurations** in your fork
3. **Test changes**: `chezmoi diff` before applying
4. **Update**: `chezmoi update` pulls latest changes

## Brewfile Maintenance

### Installing from Brewfile
```bash
# Install everything in the Brewfile
brew bundle

# Check what would be installed without installing
brew bundle --no-upgrade

# Install in a specific directory
brew bundle --file=~/dotfiles/Brewfile
```

### Updating Brewfile
```bash
# Regenerate Brewfile with current packages
brew bundle dump --force

# Add descriptions and organize (manual step)
# Then commit changes
chezmoi add Brewfile
chezmoi cd
git add Brewfile && git commit -m "Update Brewfile"
git push
```

### Cleaning Up
```bash
# List packages not in Brewfile
brew bundle cleanup --dry-run

# Remove packages not in Brewfile
brew bundle cleanup

# Update all packages
brew bundle --no-lock
```

### Checking Dependencies
```bash
# See what depends on a package
brew uses --installed <formula>

# List all leaf packages (not dependencies)
brew leaves

# Show dependency tree
brew deps --tree --installed

# Find unnecessary dependencies
brew autoremove --dry-run
```

### Best Practices
1. **Regular Updates**: Run `brew bundle dump` periodically to catch new installations
2. **Document Changes**: Add comments in Brewfile explaining why packages are needed
3. **Version Control**: Always commit Brewfile changes with descriptive messages
4. **Clean Installs**: Test Brewfile on fresh systems to ensure completeness
5. **Minimize Dependencies**: Regularly review with `brew leaves` and remove unused packages

### Example Maintenance Workflow
```bash
# 1. Check for outdated packages
brew outdated

# 2. Update everything
brew upgrade
brew upgrade --cask

# 3. Clean up old versions
brew cleanup

# 4. Regenerate Brewfile if you installed anything new
brew bundle dump --force --describe

# 5. Review and commit changes
chezmoi diff
chezmoi add Brewfile
chezmoi cd && git add -A && git commit -m "Update Brewfile after maintenance"
chezmoi git push
```

### Brewfile Structure
```ruby
# Group related packages with comments
# Development Tools
brew "git"          # Version control
brew "gh"           # GitHub CLI

# Use cask for GUI applications
cask "1password"    # Password manager

# Pin specific options when needed
brew "emacs", restart_service: :changed
```

## Troubleshooting

### Brewfile Issues
- **Missing taps**: Add required taps at the top of Brewfile
- **Conflicts**: Use `brew bundle cleanup` to identify conflicts
- **Cask errors**: Ensure `homebrew/cask` is available
- **VS Code extensions**: Require VS Code to be installed first

### SSH Key Issues
- Ensure 1Password SSH agent is running
- Check `SSH_AUTH_SOCK` points to `~/.1password/agent.sock`
- Verify keys with `ssh-add -l`

### Zsh/Prezto Issues
- Run `prezto-update` to update framework
- Check `.zpreztorc` for module configuration
- Ensure `.zshrc` sources prezto correctly