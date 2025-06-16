# Home Directory Cleanup Plan

## Goal
Move as many dotfiles as possible to XDG-compliant locations to keep `~` clean.

## XDG Base Directory Specification
- `~/.config/` - User configuration files
- `~/.local/share/` - User data files
- `~/.cache/` - Non-essential cached data
- `~/.local/state/` - State data that should persist between restarts

## Immediate Actions (Safe to Move)

### 1. Application Configs → ~/.config/
```bash
# Conda
mkdir -p ~/.config/conda
mv ~/.condarc ~/.config/conda/condarc
echo 'export CONDARC="$HOME/.config/conda/condarc"' >> ~/.zshrc

# Docker
mkdir -p ~/.config/docker
mv ~/.docker ~/.config/docker
echo 'export DOCKER_CONFIG="$HOME/.config/docker"' >> ~/.zshrc

# NPM (if exists)
mkdir -p ~/.config/npm
echo 'prefix=${HOME}/.local' > ~/.config/npm/npmrc
echo 'export NPM_CONFIG_USERCONFIG="$HOME/.config/npm/npmrc"' >> ~/.zshrc

# Git (consolidate)
mkdir -p ~/.config/git
mv ~/.gitconfig ~/.config/git/config
echo '[include]' > ~/.gitconfig
echo '    path = ~/.config/git/config' >> ~/.gitconfig
```

### 2. Cache Directories → ~/.cache/
```bash
# Yarn (if exists)
mkdir -p ~/.cache/yarn
echo 'export YARN_CACHE_FOLDER="$HOME/.cache/yarn"' >> ~/.zshrc

# Various Python tools
mkdir -p ~/.cache/pip
echo 'export PIP_CACHE_DIR="$HOME/.cache/pip"' >> ~/.zshrc
```

### 3. Data Directories → ~/.local/share/
```bash
# GnuPG
mkdir -p ~/.local/share/gnupg
echo 'export GNUPGHOME="$HOME/.local/share/gnupg"' >> ~/.zshrc
```

## Files to Keep in Home (Required)
- `.zshrc`, `.zshenv`, `.zprofile` - Shell startup files
- `.gitconfig` - Git looks here first (can be minimal with includes)
- `.ssh/` - SSH expects this location
- `.DS_Store` - macOS system file

## Chezmoi Management Strategy

### Add Environment Variables Template
Create `~/.config/shell/xdg-env.sh`:
```bash
# XDG Base Directory Specification
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Application-specific XDG compliance
export CONDARC="$XDG_CONFIG_HOME/conda/condarc"
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
export JUPYTER_CONFIG_DIR="$XDG_CONFIG_HOME/jupyter"
export IPYTHONDIR="$XDG_CONFIG_HOME/ipython"
export PYLINTHOME="$XDG_CACHE_HOME/pylint"
export PYTHONSTARTUP="$XDG_CONFIG_HOME/python/pythonrc"
```

### Update .zshrc
Add near the top:
```bash
# XDG compliance
[ -f "$HOME/.config/shell/xdg-env.sh" ] && source "$HOME/.config/shell/xdg-env.sh"
```

## Implementation Steps

1. **Backup current setup**
   ```bash
   chezmoi git -- add -A && chezmoi git -- commit -m "Backup before XDG migration"
   ```

2. **Create XDG directories**
   ```bash
   mkdir -p ~/.config/{conda,docker,npm,git,shell}
   mkdir -p ~/.cache/{pip,yarn}
   mkdir -p ~/.local/share/gnupg
   ```

3. **Move configs with chezmoi**
   - Add new locations to chezmoi
   - Create environment variable file
   - Update shell configs

4. **Test thoroughly**
   - Open new terminal
   - Verify all tools work
   - Check moved configs are found

## Result
After cleanup, your home directory will primarily contain:
- Essential shell configs (.zshrc, etc.)
- System files (.DS_Store, .CFUserTextEncoding)
- Minimal stub files that point to ~/.config

Most application data will be organized under:
- `~/.config/` - Configurations
- `~/.local/` - Data and binaries
- `~/.cache/` - Temporary files