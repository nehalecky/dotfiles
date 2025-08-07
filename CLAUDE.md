# Claude Code Instructions - Dotfiles Repository

## Primary Development Workflows

### 1. Discovery-First Development
**When:** Complex features or unfamiliar codebases  
**Process:** Explore → Plan → Confirm → Code → Commit
- Use search tools extensively to understand the codebase
- Create a TodoWrite plan before implementation
- Present the plan to user for confirmation
- Implement with confidence
- Commit with descriptive message

### 2. Test-Driven Workflow
**When:** Adding new functionality with clear requirements  
**Process:** Write tests → Commit → Code → Iterate → Commit
- Write failing tests first
- Commit the tests
- Implement code to pass tests
- Refactor and iterate
- Commit working implementation

### 3. Visual Feedback Loop
**When:** UI/UX development or visual outputs  
**Process:** Write code → Screenshot → Iterate
- Implement initial version
- Use screenshot tools or Puppeteer for visual feedback
- Iterate based on visual results
- Perfect the output through rapid cycles

## Repository Context

**Stack:** macOS, Zsh/Prezto, Starship prompt, WezTerm, chezmoi, uv (Python)  
**TUI Tools:** yazi, helix, k9s, lazydocker, delta, dust, procs, bandwhich, atac, zellij  
**Security:** 1Password for SSH/secrets, SSH commit signing  
**Philosophy:** Ultra-modern terminal-first development, aggressive performance optimization

## Specific Instructions

### Chezmoi Operations
- Always use `$HOME` not `/Users/username` in paths
- Run `chezmoi diff` before `chezmoi apply`
- Use templates (`.tmpl`) for machine-specific configs
- Store machine variations in `.chezmoidata.yaml`

### Code Standards
- Use 2-space indentation for shell scripts
- Comment non-obvious configuration choices
- Group related settings with clear headers
- Never commit secrets or credentials

### Git Practices
- Descriptive commit messages explaining "why"
- Reference issues/PRs when applicable
- Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`
- Always sign commits (GPG configured)

### Tool Preferences
- Use ripgrep (`rg`) not grep
- Use `eza` not `ls` for listings
- Use `bat` not `cat` for file viewing
- Verify tool docs with WebFetch before suggesting commands

## Quick Reference

### Common Tasks

**Primary Workflow** (HOME → Source - always use this):
```bash
vim ~/.zshrc                    # Edit actual file in HOME
chezmoi add ~/.zshrc           # Sync changes to source
chezmoi git -- commit -m "msg" # Commit
chezmoi git -- push           # Push
```

**Advanced Workflow** (Source → HOME - only for complex batch changes):
```bash
chezmoi edit ~/.zshrc          # Edit source file directly
chezmoi diff                   # Preview changes  
chezmoi apply                  # Apply to HOME (verify success!)
chezmoi git -- commit -m "msg" # Commit
chezmoi git -- push           # Push
```

**Sync from Remote**:
```bash
chezmoi update                 # Pull + apply
# OR
chezmoi git pull              # Just pull
chezmoi diff                  # Preview
chezmoi apply                 # Apply
```

**Modern TUI Workflow** (WezTerm leader key shortcuts):
```bash
Ctrl+a f                      # File manager (yazi)
Ctrl+a e                      # Editor (helix)
Ctrl+a g                      # Git (lazygit)
Ctrl+a k                      # Kubernetes (k9s)
Ctrl+a d                      # Docker (lazydocker)
Ctrl+a a                      # API client (atac)
Ctrl+a w                      # Launch 4-tile development workspace
dev-workspace [project]       # Automated project setup
```

### Key Files
- `Brewfile` - Homebrew dependencies (67+ packages including modern TUI tools)
- `.chezmoidata.yaml` - Machine-specific variables
- `dot_config/starship.toml.tmpl` - Ultra-fast prompt configuration
- `.wezterm.lua` - Terminal multiplexer with leader key shortcuts
- `dot_local/bin/executable_dev-workspace` - Automated workspace setup
- `.chezmoiscripts/` - Installation hooks

## Development Guidelines

1. **Ask before creating** - Propose new tools/scripts before implementing
2. **Enhance, don't add** - Improve existing tools over adding new ones
3. **Document changes** - Update relevant .md files when making changes
4. **Test everything** - Verify commands work before suggesting
5. **Keep it portable** - Ensure configs work across machines
6. **Test before committing** - Always test scripts/commands fully before committing
7. **Clean commit history** - Amend commits for small fixes; comprehensive messages
8. **Use chezmoi commands** - Always use `chezmoi git` from $HOME, not `cd && git`

## MCP Integrations

### MCP Server Installation Process
**CRITICAL: Always start with a general search first - MCP integration is straightforward and shouldn't be confusing after proper research.**

**Required Process:**
1. **General Search First**: Search "[service] MCP server" to understand what's available
2. **Find Official Documentation**: Look for official installation instructions (e.g., service.com/settings/mcp)
3. **Use Standard Tooling**: Apply `claude mcp add` with appropriate transport and authentication
4. **Validate Properly**: Only claim success when `claude mcp list` shows "✓ Connected"

**Never:**
- Skip the initial general search
- Use custom npm packages when official servers exist
- Claim success without proper validation
- Overcomplicate what should be simple

### Example MCP Servers
**GitHub:** `claude mcp add github github.com/github/github-mcp-server`
**Hugging Face:** `claude mcp add hf-mcp-server -t http "https://huggingface.co/mcp" -H "Authorization:Bearer $(op read 'op://Private/[token]/credential')"`

*Note: These are examples only - the process applies to any MCP server installation.*

## Current Focus Areas
- Terminal productivity enhancements
- Security hardening without friction
- Development workflow optimization
- Cross-platform compatibility prep
- GitHub integration workflow enhancement

## Workflow Principles
- **HOME → Source workflow**: Always edit files in HOME directory, then sync to source with `chezmoi add`
- **Verify apply success**: When using source → HOME workflow, always verify `chezmoi apply` succeeds
- Always leverage existing workflows, including chezmoi apply, so we don't unnecessarily complicate things
- Use MCP integrations to reduce context switching between tools

---
@docs/important-instruction-reminders.md