# Claude AI Assistant Instructions

This file provides context and instructions for Claude when working with this dotfiles repository.

## Repository Overview

This is a modern dotfiles setup using [chezmoi](https://chezmoi.io/) for managing configuration files across machines. The repository emphasizes security, maintainability, and documentation.

## Key Architecture Decisions

### Dotfiles Management
- **Tool**: chezmoi (replaced bare git repo approach)
- **Structure**: Actual file content, not symlinks
- **Location**: `~/.local/share/chezmoi/`

### Security
- **SSH Keys**: Stored in 1Password, never on disk
- **SSH Agent**: 1Password agent at `~/.1password/agent.sock`
- **Git Signing**: GPG keys managed via GPG Suite

### Shell Environment
- **Shell**: Zsh with Prezto framework
- **Prompt**: Powerlevel10k (planning to migrate to Starship)
- **Enhancements**: bat, eza, ripgrep, fzf

## Working with This Repository

### Common Tasks

1. **Adding new dotfiles**:
   ```bash
   chezmoi add ~/.config/newapp/config
   ```

2. **Updating configurations**:
   ```bash
   chezmoi edit ~/.zshrc
   chezmoi diff
   chezmoi apply
   ```

3. **Syncing changes**:
   ```bash
   chezmoi git add .
   chezmoi git commit -m "Update configurations"
   chezmoi git push
   ```

### Important Files

- `Brewfile` - All Homebrew dependencies
- `APPLICATIONS.md` - Detailed documentation of all tools
- `homebrew-analysis.md` - Dependency analysis
- `.zshrc` - Main shell configuration
- `.gitconfig` - Git configuration with signing

## Preferences and Standards

### Code Style
- Clear, commented configurations
- Group related settings with headers
- Document non-obvious choices

### Git Commits
- Descriptive commit messages
- Include what changed and why
- Reference issues when applicable

### Documentation
- Keep README concise but complete
- Detailed docs in separate files
- Include examples and use cases

## System Context

### Development Focus
- **Languages**: Python, JavaScript/Node.js, Shell scripting
- **Tools**: Docker, Git, GitHub CLI
- **Editors**: VS Code, Cursor (AI-assisted), Emacs

### Workflow Preferences
- Terminal-first approach
- Keyboard shortcuts over GUI
- Automation where sensible
- Security without friction

## AI Assistant Guidelines

When helping with this repository:

1. **Maintain existing patterns** - Follow established conventions
2. **Document changes** - Update relevant documentation files
3. **Test before applying** - Use `chezmoi diff` to preview
4. **Security first** - Never expose secrets or credentials
5. **Explain decisions** - Document why changes were made
6. **Verify before suggesting** - Always check documentation before suggesting commands
   - Use WebFetch to verify tool documentation
   - Provide clickable URLs for references (iTerm2 will make them clickable!)
   - Ground suggestions in actual documentation, not assumptions
   - Example: https://iterm2.com/documentation-shell-integration.html
7. **Consult before creating tools** - Always ask before building new tools or scripts
   - Use existing tools (especially chezmoi) as the primary interface
   - Leverage chezmoi's built-in features (hooks, scripts, templates)
   - Avoid creating separate management tools
8. **Chezmoi-first approach** - Use chezmoi's native capabilities
   - Hooks for automation (e.g., checking Brewfile updates)
   - Scripts for complex workflows
   - Templates for dynamic configuration
9. **Present proposals before implementing** - Always explain the approach first
   - Describe what you plan to do and why
   - Wait for approval before implementing
   - Avoid over-engineering - simpler is better
   - Question if additional tools/functions are truly needed
10. **Keep code portable** - Never use hardcoded paths
   - Always use `$HOME` instead of `/Users/username`
   - This ensures dotfiles work for any user
   - Check all documentation for hardcoded references
11. **Always leverage existing workflows** - Don't recreate what chezmoi already does
   - Use `chezmoi apply` - it runs all hooks automatically (e.g., Brewfile sync)
   - Never manually run hook scripts - they execute on their own
   - Trust chezmoi's automation - hooks run after every `chezmoi apply`
   - When installing new tools via brew, the Brewfile hook will auto-detect on next `chezmoi apply`
   - Example: After `brew install lazygit`, just continue working. The next `chezmoi apply` will detect and prompt to sync
12. **ALWAYS check paths in documentation** - Never use hardcoded usernames
   - WRONG: `/Users/nehalecky/docs/file.md`
   - RIGHT: `~/.docs/file.md` or `.docs/file.md` (relative)
   - RIGHT: `$HOME/.docs/file.md` (when full path needed)
   - Check ALL documentation updates for hardcoded paths
   - This includes README, docs, and any generated content
   - The user has specifically requested this multiple times

### Helpful Context

- User prefers minimal dependencies
- Performance and security are priorities
- Documentation should be comprehensive
- Changes should be version controlled

### Common Improvements

When asked to enhance the setup, consider:
- Terminal productivity tools
- Security hardening
- Development workflow optimization
- Documentation updates
- Dependency minimization

## Future Enhancements Under Consideration

1. **Starship configuration** - Custom prompt setup
2. **Neovim migration** - Potential editor change
3. **Tmux configuration** - Terminal multiplexing
4. **Automated testing** - Validate dotfiles work correctly
5. **Cross-platform support** - Linux compatibility

## Notes for Claude

- The user values clean, well-documented code
- Prefer enhancing existing tools over adding new ones
- Always consider security implications
- Keep backups before major changes
- Test commands before suggesting them

---

*This file helps Claude understand the repository structure and user preferences for more effective assistance.*