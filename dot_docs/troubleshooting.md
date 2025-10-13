# Troubleshooting

Common issues, solutions, and debugging workflows for this development environment.

## General Debugging

### Chezmoi Issues

**Sync problems**:
```bash
chezmoi doctor               # Diagnose configuration issues
chezmoi status               # Check what's changed
chezmoi diff                 # See specific differences
```

**Files not applying correctly**:
1. Check for syntax errors in template files
2. Verify `.chezmoidata.yaml` has correct values
3. Review `.chezmoiignore` for unintended excludes

**Git integration issues**:
```bash
chezmoi git -- status        # Check repository status
chezmoi git -- log          # View commit history
```

**Course correction for wrong workflow**:
If you accidentally edited in `~/.local/share/chezmoi/` instead of HOME:
```bash
# Copy changes back to HOME
cp ~/.local/share/chezmoi/dot_file ~/.file
# Test in HOME
source ~/.file               # Or appropriate test
# Re-sync with correct workflow
chezmoi add ~/.file
```

### Tool Installation Problems

**Missing packages**:
```bash
brew bundle check            # See what's missing
brew bundle install          # Install missing packages
```

**Homebrew diagnostics**:
```bash
brew doctor                  # Configuration health check
brew update                  # Update package definitions
brew upgrade                 # Upgrade installed packages
```

**Installation failures**:
1. Check available disk space
2. Verify Xcode Command Line Tools installed
3. Review Homebrew logs: `brew --prefix`/var/log/brew/

### Authentication Issues

**GitHub CLI authentication**:
```bash
gh auth status               # Check authentication status
gh auth login                # Re-authenticate if needed
gh auth refresh              # Refresh existing credentials
```

**1Password SSH agent**:
1. Ensure 1Password app is running
2. Check SSH agent configuration:
   ```bash
   ssh-add -L                # List loaded keys
   ```
3. Verify `~/.config/1Password/ssh/agent.toml` exists
4. Restart 1Password if keys not loading

**Git commit signing failures**:
```bash
# Verify SSH signing configuration
git config --get gpg.format           # Should show 'ssh'
git config --get user.signingkey      # Should show your key path

# Test signing
echo "test" | ssh-keygen -Y sign -n git -f ~/.ssh/id_ed25519_signing
```

## Specific Tool Issues

### Terminal/Shell

**Leader key not working (Ctrl+a)**:
1. Verify WezTerm is running (not another terminal)
2. Check if another application is capturing `Ctrl+a`
3. Try restarting WezTerm: `Cmd+Q` then relaunch
4. Verify configuration loaded:
   ```bash
   grep -A5 "leader_key" ~/.config/wezterm/wezterm.lua
   ```

**Slow prompt**:
- Check starship modules are optimized:
  ```bash
  starship timings            # Show module execution times
  ```
- Verify git repositories aren't too large
- Disable expensive prompt modules temporarily:
  ```bash
  # Edit ~/.config/starship.toml
  vim ~/.config/starship.toml
  ```

**Prezto/zsh configuration not loading**:
1. Verify `.zshrc` sources prezto:
   ```bash
   grep zprezto ~/.zshrc
   ```
2. Check prezto installation:
   ```bash
   ls -la ~/.zprezto
   ```
3. Reload shell configuration:
   ```bash
   source ~/.zshrc
   ```

### Python Development

**uv not found or not working**:
```bash
# Verify installation
which uv

# Reinstall if missing
brew install uv

# Check version
uv --version
```

**Virtual environment activation issues**:
```bash
# Manually activate if needed
source .venv/bin/activate

# Recreate environment
uv venv --python 3.12
```

**Package installation failures**:
```bash
# Clear cache
uv cache clean

# Verbose installation for debugging
uv pip install package-name --verbose

# Try different Python version
uv venv --python 3.11
```

**uv sync errors**:
1. Check `pyproject.toml` syntax
2. Verify Python version compatibility
3. Review error messages for conflicting dependencies

### Git/Version Control

**Commit signing failures**:
1. Verify 1Password SSH agent is running
2. Check signing key exists:
   ```bash
   ls -la ~/.ssh/id_ed25519_signing*
   ```
3. Test SSH signing:
   ```bash
   echo "test" | ssh-keygen -Y sign -n git -f ~/.ssh/id_ed25519_signing
   ```

**Push/pull authentication issues**:
```bash
gh auth status               # Check GitHub CLI status
gh auth refresh              # Refresh credentials
ssh -T git@github.com        # Test SSH connection
```

**lazygit not working**:
1. Verify installation: `which lazygit`
2. Check git configuration: `git config --list`
3. Launch with debug: `lazygit --debug`

## Claude Code Integration

### Memory System Issues

**Project CLAUDE.md not found**:
```bash
# Generate for current project
python3 ~/.claude/memories/templates/generator.py .

# Verify memory system exists
ls -la ~/.claude/memories/
```

**Memory module imports failing**:
```bash
# Check project CLAUDE.md imports
grep '^@' CLAUDE.md

# Verify referenced modules exist
ls ~/.claude/memories/workflows/
ls ~/.claude/memories/tools/
```

**Generator script errors**:
```bash
# Test generator directly
python3 ~/.claude/memories/templates/generator.py --help

# Verify Python can import modules
python3 -c "
from pathlib import Path
import sys
sys.path.append(str(Path.home() / '.claude/memories/templates'))
from generator import ProjectDetector
print('Import successful')
"
```

### Agent Integration Issues

**Slash commands not working**:
1. Check commands directory exists:
   ```bash
   ls ~/.claude/commands/
   ```
2. Verify command files have `.md` extension
3. Reload Claude Code configuration

**Hooks not executing**:
```bash
# Verify hooks directory
ls ~/.claude/hooks/

# Check hook permissions
ls -la ~/.claude/hooks/*.py

# Test hook manually
python3 ~/.claude/hooks/pre_tool_use.py
```

## Performance Issues

### High CPU Usage

**Identify resource-heavy processes**:
```bash
btop                         # Interactive process monitor
top                          # Built-in process viewer
```

**Common culprits**:
- Runaway background tasks from TUI tools
- Infinite loops in shell startup scripts
- File watching services on large directories

### Memory Usage

**Quick fixes**:
- Exit unused TUI applications with `q`
- Restart WezTerm periodically: `Cmd+Q` then relaunch
- Close inactive workspace panes

**Investigate memory leaks**:
```bash
# Check memory usage by process
ps aux | sort -k4 -r | head -10

# Monitor in real-time
btop
```

### Slow File Operations

**Check disk performance**:
```bash
df -h                        # Disk space
diskutil info disk0          # Disk details
```

**Large git repositories**:
- Run `git gc` to optimize repository
- Consider shallow clones for large repos
- Use `.gitignore` to exclude build artifacts

## Workspace Issues

### Workspace Scripts Not Found

**Verify installation**:
```bash
which workspace-home         # Should show ~/.local/bin/workspace-home
which workspace-dev          # Should show ~/.local/bin/workspace-dev
```

**Reinstall if missing**:
```bash
chezmoi apply ~/.local/bin/
chmod +x ~/.local/bin/workspace-*
```

### Workspace Layout Problems

**Panes not spawning correctly**:
1. Check WezTerm configuration syntax
2. Verify commands in workspace script exist
3. Review WezTerm logs: `tail -f ~/.local/share/wezterm/wezterm.log`

**Project detection not working**:
```bash
# Debug workspace-dev detection
cd /path/to/project
cat workspace-dev            # Review detection logic
```

## Getting Help

### Documentation Resources

- **[Tool Reference](tool-reference.md)** - Complete command and shortcut reference
- **[README](README.md)** - Overview and quick start
- **[System Architecture](architecture.md)** - System design details
- **[Setup Guide](setup-guide.md)** - First-time setup and customization

### Diagnostic Commands

Run these to gather debugging information:

```bash
# Configuration health checks
chezmoi doctor               # Chezmoi configuration
brew doctor                  # Homebrew diagnostics
gh auth status              # GitHub authentication

# Version information
uv --version                 # Python package manager
node --version               # Node.js
brew --version               # Homebrew

# System information
uname -a                     # Operating system
sw_vers                      # macOS version
```

### Log Locations

- **Homebrew logs**: `$(brew --prefix)/var/log/brew/`
- **WezTerm logs**: `~/.local/share/wezterm/wezterm.log`
- **Claude Code logs**: `~/.claude/data/logs/`
- **Shell history**: `~/.zsh_history`

### Community Resources

- **Tool documentation**: Run `tool --help` for any installed command
- **GitHub issues**: File tool-specific problems with respective projects
- **chezmoi docs**: [chezmoi.io](https://www.chezmoi.io/) for dotfile management
- **Homebrew docs**: [brew.sh](https://brew.sh/) for package management

### When to File Issues

File issues on GitHub when you encounter:
- Reproducible bugs in custom scripts
- Configuration problems affecting multiple machines
- Documentation gaps or errors
- Feature requests for workspace improvements

**Include in issue reports**:
- Output of relevant diagnostic commands
- Steps to reproduce the problem
- Expected vs actual behavior
- System information (`sw_vers`, relevant tool versions)
