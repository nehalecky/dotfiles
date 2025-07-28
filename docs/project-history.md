# Dotfiles Project History

This document tracks the evolution of this dotfiles repository in reverse chronological order.

## 2025-07-28: SSH Commit Signing Implementation
- **Goal**: Enable verified commits using existing 1Password SSH infrastructure
- **Decision**: Use SSH commit signing instead of GPG
- **Rationale**:
  - Leverages existing 1Password SSH setup (keys already configured)
  - Simpler than GPG key management and distribution
  - Consistent with existing authentication workflow
  - Supported natively by GitHub since 2022
- **Changes Made**:
  - Created `dot_config/git/config` with SSH signing configuration
  - Configured `gpg.format = ssh` and 1Password SSH signing program
  - Used existing "Github Signing Key (Nico Personal)" from 1Password
- **Benefits**: Single key management system, consistent with auth workflow

## 2025-07-28: Prezto Installation Automation
- **Goal**: Document prezto setup approach and add automation
- **Issue**: Prezto installation was manual, not automated in chezmoi setup
- **Decision**: Use upstream prezto repository, not a fork
- **Rationale**:
  - No need to maintain a fork in sync with upstream
  - All customizations managed through `.zpreztorc` (chezmoi-managed)
  - Cleaner updates - pull directly from source
  - Follows best practice of separating framework from configuration
- **Changes Made**:
  - Added `.chezmoiexternal.yaml` for automatic prezto installation
  - Updated documentation to reflect automated approach
- **Lesson Learned**: Manual steps should be automated in chezmoi

## 2025-05-24: Architecture Documentation & Chezmoi-First Workflows
- **Goal**: Create clear architecture visualization and leverage chezmoi for workflows
- **Changes Made**:
  - Created comprehensive `ARCHITECTURE.md` with diagrams
  - Added chezmoi hook to check Brewfile updates
  - Updated CLAUDE.md to require consultation before creating tools
  - Modified README to show chezmoi workflows
  - Removed custom tool in favor of chezmoi's native capabilities
- **Key Features**:
  - Visual architecture at multiple levels (100K' and detailed)
  - Chezmoi hooks for automation
  - Native chezmoi commands for all workflows
- **Lessons Learned**:
  - Don't reinvent the wheel - chezmoi is already the management tool
  - Use hooks and scripts within chezmoi's framework
  - Always consult before creating new tools

## 2025-05-24: README Modernization & Cleanup
- **Goal**: Create a clean, modern README focused on current state
- **Changes Made**:
  - Removed all migration/legacy sections (moved to project history)
  - Added Homebrew installation command
  - Created dedicated sections for Secrets and Dependency Management
  - Replaced hardcoded paths with `$HOME` throughout
  - Added links to all referenced tools and documentation
  - Emphasized prerequisites and quick setup
  - Streamlined content to essentials only
- **Key Improvements**:
  - Clear entry point with Homebrew installation
  - Prominent secrets management section
  - All tools properly linked to documentation
  - Focus on current state, not history

## 2025-05-24: Hybrid Secrets Management Strategy
- **Goal**: Create a flexible secrets system with 1Password as canonical source
- **Changes Made**:
  - Designed hybrid approach: 1Password (primary) + encrypted files (fallback)
  - Rewrote `SECRETS-MANAGEMENT.md` with comprehensive hybrid strategy
  - Created environment detection templates using `lookPath`
  - Documented sync workflow from 1Password to encrypted files
  - Added automation scripts for secret synchronization
- **Key Innovation**:
  - Templates automatically detect environment capabilities
  - Single source of truth (1Password) with secure fallback
  - Works in both development (with 1Password) and restricted environments
- **Security Analysis**:
  - No hardcoded secrets found in current dotfiles
  - Already using 1Password for SSH and Git signing
  - Clean environment with security best practices

## 2025-05-24: 1Password Integration Setup
- **Goal**: Integrate chezmoi with 1Password for secure secrets management
- **Changes Made**:
  - Created `.install-1password-cli.sh` hook to ensure 1Password CLI availability
  - Added `chezmoi.toml` configuration for 1Password integration
  - Created initial `SECRETS-MANAGEMENT.md` documentation
  - Added example `.env.tmpl` template for environment variables
  - Set up framework for hybrid secrets (1Password + age encryption)
- **References**:
  - https://www.chezmoi.io/user-guide/password-managers/1password/
  - https://www.chezmoi.io/user-guide/advanced/install-your-password-manager-on-init/

## 2025-05-23: Documentation Accuracy Improvement
- **Goal**: Ensure AI assistance is grounded in actual documentation
- **Changes Made**:
  - Removed incorrectly created `setup-iterm2-integration.sh` based on hallucinated "it2" commands
  - Updated CLAUDE.md to emphasize documentation verification
  - Added guideline to provide clickable URLs for references
- **Lessons Learned**:
  - Always verify tool capabilities against official documentation
  - iTerm2 shell integration uses functions, not CLI commands
  - Documentation links: https://iterm2.com/documentation-shell-integration.html

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