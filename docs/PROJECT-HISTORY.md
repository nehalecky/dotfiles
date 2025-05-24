# Dotfiles Project History

This document tracks the evolution of this dotfiles repository in reverse chronological order.

## 2025-05-23: Bare Repo Archive & Final Cleanup
- **Goal**: Complete migration from bare repo to chezmoi
- **Changes Made**:
  - Archived bare repo `.dotfiles-config/` to `~/Repos/dotfiles-config-bare-repo-archive`
  - Removed `dotfiles` alias from `.zshrc`
  - Preserved legacy setup instructions in `docs/LEGACY-SETUP-NOTES.md`
  - Cleaned up duplicate `~/Brewfile` and `~/scripts/` (already in chezmoi)
  - Confirmed VS Code and Cursor are both in Brewfile
- **Lessons Learned**:
  - Legacy bare repo contained valuable setup documentation
  - iTerm2 setup and GPG key instructions worth preserving
  - Clean transition from bare repo to chezmoi completed

## 2025-05-23: Home Directory Cleanup & XDG Migration
- **Goal**: Clean up legacy dotfiles and migrate to XDG Base Directory spec
- **Changes Made**:
  - Migrated configurations to XDG directories:
    - `~/.gnupg` → `~/.local/share/gnupg`
    - `~/.gitignore` → `~/.config/git/ignore`
    - `~/.fzf.*` → `~/.config/fzf/`
    - `~/.iterm2_shell_integration.zsh` → `~/.config/iterm2/`
  - Removed legacy/unused directories (freed ~180MB):
    - `.atom`, `.mono`, `.theano`, `.sonic-pi`, `.gnupg_pre_2.1`
    - `.ipynb_checkpoints`, `.matplotlib`, `.cups`, `.julia`, `.pixi`, `.emacs.d`
  - Created minimal `.bashrc` for compatibility
  - Kept security-critical `.sigstore` directory
- **Lessons Learned**:
  - Many tools already support XDG (git, npm, docker, etc.)
  - Some files must stay in home (shell configs, .ssh)
  - `.npm` auto-recreates when npm runs
  - Research before removing security-related directories

## 2025-05-23: Documentation Reorganization
- **Goal**: Create organized documentation structure
- **Changes Made**:
  - Created `docs/` directory for all documentation
  - Moved all .md files from home to `docs/`
  - Created symlinks in home for README.md and CLAUDE.md
  - Added PROJECT-HISTORY.md for tracking changes
  - Created docs/README.md as documentation index
- **Structure**:
  - `~/README.md` → `~/docs/ROOT-README.md` (symlinked)
  - `~/CLAUDE.md` → `~/docs/CLAUDE.md` (symlinked)
  - All other docs moved to `docs/` without symlinks
- **Lessons Learned**:
  - Symlinks maintain compatibility while organizing files
  - Separating current state (README) from history improves clarity
  - Central docs directory makes maintenance easier

## 2025-05-23: Python Environment Migration
- **Goal**: Migrate from Miniconda to uv for Python management
- **Changes Made**:
  - Removed conda initialization from `.zshrc`
  - Uninstalled Miniconda via Homebrew
  - Installed uv (v0.7.7) as the new Python package manager
  - Cleaned up conda directories (`~/.conda`)
  - Documented old conda environments for reference
- **Lessons Learned**:
  - 1Password brew plugin alias was intercepting brew commands
  - uv provides faster, more modern Python environment management
  - Old conda environments from 2021-2022 were no longer needed

## 2025-05-22: XDG Base Directory Preparation
- **Goal**: Begin migration to XDG Base Directory specification
- **Changes Made**:
  - Created `.config/shell/xdg-env.sh` with XDG environment variables
  - Set up proper XDG directory structure
  - Updated `.zshrc` to source XDG environment early
- **Next Steps**:
  - Move remaining dotfiles to appropriate XDG directories
  - Update application configurations to use XDG paths

## 2025-05-22: Initial Documentation Structure
- **Goal**: Establish comprehensive documentation
- **Changes Made**:
  - Created `CLAUDE.md` for AI assistant context
  - Created `APPLICATIONS.md` with detailed tool documentation
  - Created `homebrew-analysis.md` for dependency tracking
  - Updated `README.md` with current setup instructions
- **Lessons Learned**:
  - Detailed documentation helps with maintenance
  - Separating concerns into different documents improves clarity

## Historical Context

### Previous Setup (Pre-2025)
- Used Miniconda for Python environment management
- Dotfiles scattered in home directory
- Limited documentation
- Manual configuration management

### Migration Motivations
1. **XDG Compliance**: Cleaner home directory, better organization
2. **Modern Tools**: Replace older tools with faster alternatives (uv vs conda)
3. **Documentation**: Maintain clear history and instructions
4. **Automation**: Move towards more automated setup processes