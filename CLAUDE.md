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

**Stack:** macOS, Zsh/Prezto, Powerlevel10k prompt, chezmoi, uv (Python)  
**Security:** 1Password for SSH/secrets, GPG for signing  
**Philosophy:** Terminal-first, minimal dependencies, security without friction

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

**Quick Edit** (edit in home, sync to source):
```bash
vim ~/.zshrc                    # Edit actual file
chezmoi add ~/.zshrc           # Update source
chezmoi git commit -- -m "msg"  # Commit
chezmoi git push               # Push
```

**Structured Edit** (edit in source, test, apply):
```bash
chezmoi edit ~/.zshrc          # Edit source file
chezmoi diff                   # Preview changes
chezmoi apply                  # Apply to home
chezmoi git commit -- -m "msg"  # Commit
chezmoi git push               # Push
```

**Sync from Remote**:
```bash
chezmoi update                 # Pull + apply
# OR
chezmoi git pull              # Just pull
chezmoi diff                  # Preview
chezmoi apply                 # Apply
```

### Key Files
- `Brewfile` - Homebrew dependencies
- `.chezmoidata.yaml` - Machine-specific variables
- `dot_config/starship.toml.tmpl` - Prompt configuration
- `.chezmoiscripts/` - Installation hooks

## Development Guidelines

1. **Ask before creating** - Propose new tools/scripts before implementing
2. **Enhance, don't add** - Improve existing tools over adding new ones
3. **Document changes** - Update relevant .md files when making changes
4. **Test everything** - Verify commands work before suggesting
5. **Keep it portable** - Ensure configs work across machines

## MCP Integrations

### GitHub MCP Server
**Purpose:** Direct GitHub integration within Claude Code  
**Capabilities:**
- Repository browsing and file access
- Issue and PR management (create, update, close)
- Code review assistance and PR descriptions
- CI/CD status monitoring
- Release management and notes generation

**Usage Examples:**
```bash
# Direct GitHub operations in Claude
"Create a GitHub issue for this bug"
"Show me open PRs in my dotfiles repo"
"Help write a PR description for these changes"
"Check the latest release of any GitHub repo"
```

**Configuration:** Added via `claude mcp add github github.com/github/github-mcp-server`

## Current Focus Areas
- Terminal productivity enhancements
- Security hardening without friction
- Development workflow optimization
- Cross-platform compatibility prep
- GitHub integration workflow enhancement

## Workflow Principles
- Always leverage existing workflows, including chezmoi apply, so we don't unnessarily complicate things
- Use MCP integrations to reduce context switching between tools

---
@docs/important-instruction-reminders.md