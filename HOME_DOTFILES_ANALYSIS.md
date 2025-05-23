# Home Directory Dotfiles Analysis

## Current Status
Total dotfiles/directories in ~: 54

## Migration Categories

### ✅ Already Handled by Migration Script
- `.condarc` → `~/.config/conda/condarc`
- `.docker/` → `~/.config/docker/`
- `.ipython/` → `~/.config/ipython/`
- `.jupyter/` → `~/.config/jupyter/`
- `.matplotlib/` → `~/.config/matplotlib/`
- `.gnupg/` → `~/.local/share/gnupg/`
- `.julia/` → `~/.local/share/julia/`

### 🔧 Additional Configs to Migrate
```bash
# NPM
.npm/ → ~/.config/npm/

# Yarn
.yarn/ → ~/.config/yarn/

# VS Code (already uses standard location on macOS)
.vscode/ → Keep (VS Code expects it here on macOS)

# Cursor
.cursor/ → ~/.config/cursor/
.cursor-tutor/ → ~/.config/cursor-tutor/

# Atom (if still used)
.atom/ → ~/.config/atom/

# Claude
.claude.json → ~/.config/claude/config.json
.claude/ → ~/.cache/claude/  # appears to be cache

# Python
.ipynb_checkpoints/ → ~/.cache/jupyter/checkpoints/
.theano/ → ~/.cache/theano/
.pixi/ → ~/.config/pixi/

# Other dev tools
.mono/ → ~/.config/mono/
.sonic-pi/ → ~/.config/sonic-pi/
```

### 📁 Keep in Home (Required/Expected)
```bash
# Shell (must be in ~)
.zshrc, .zshenv, .zprofile, .zlogin, .zlogout
.bashrc, .bash_profile
.zprezto/, .zpreztorc
.p10k.zsh

# SSH (expected location)
.ssh/

# Git (can use include)
.gitconfig

# System/macOS
.CFUserTextEncoding  # macOS system file
.DS_Store           # macOS Finder
.Trash/             # macOS Trash

# Already XDG compliant
.config/
.cache/
.local/

# Special purpose
.1password/         # 1Password agent
.dotfiles-config/   # Your bare git repo
```

### 🗑️ Can Be Cleaned Up
```bash
.gitignore          # Use ~/.config/git/ignore instead
.README.md          # Unusual location
.gnupg_pre_2.1/     # Old backup
.fzf.bash          # If not using bash
.fzf.zsh           # Source from .config instead
.lesshst           # Move to XDG_STATE_HOME
.wget-hsts         # Move to XDG_CACHE_HOME
.zhistory          # Duplicate of .zsh_history?
.emacs.d/          # If not using emacs
.cups/             # Printing, rarely needed
.sigstore/         # If not using sigstore
```

### 📊 Summary After Migration
**Before**: 54 items in ~
**After**: ~25 items in ~ (mostly shell configs and system files)
**Reduction**: ~54% cleaner home directory

### 🎯 Recommended Actions
1. Run the migration script for supported apps
2. Manually migrate additional configs listed above
3. Clean up unused/legacy files
4. Update environment variables for each app
5. Test each application after migration