# Claude Code Instructions - Dotfiles Repository

## CRITICAL WORKFLOW ENFORCEMENT

**YOU MUST follow this decision tree before ANY file operation:**

### MANDATORY PRE-ACTION CHECK:
**IMPORTANT:** Read this section EVERY TIME before creating/editing files.

1. **FILE LOCATION CHECK**:
   - Am I about to create/edit in `~/.local/share/chezmoi/`? → **STOP! WRONG WORKFLOW**
   - Am I editing in HOME directory first? → **CONTINUE**

2. **WORKFLOW VERIFICATION**:  
   - New file: Create in HOME → Test → `chezmoi add` → Commit
   - Existing file: Edit in HOME → Test → `chezmoi add` → Commit

**Course Correction:** When you catch yourself about to write to `/Users/nehalecky/.local/share/chezmoi/`, STOP and use the HOME→Source workflow instead.


## Core Development Context

### Essential Workflow Modules (Auto-Loaded)
@.claude/memories/workflows/core-workflows.md
@.claude/memories/tools/essential-tools.md
@.claude/memories/tools/git-standards.md

### Environment Context
**Platform:** macOS with Zsh shell
**Package Managers:** uv (Python), Homebrew (macOS)
**Core Tools:** rg, fd, eza, bat, delta (CLI tools Claude Code can execute)
**Dotfiles:** chezmoi-managed (HOME→Source workflow mandatory)
**Git:** SSH commit signing enforced

### Code Standards
- 2-space indentation for shell scripts
- Comment non-obvious configuration choices
- Group related settings with clear headers
- Never commit secrets or credentials

### Workflow Principles
- **HOME → Source workflow**: Always edit files in HOME directory first, then `chezmoi add`
- **Verify success**: When using source → HOME workflow, verify `chezmoi apply` succeeds
- **Ask before creating** new tools/scripts - prefer enhancing existing ones
- **Test everything** before suggesting commands
- **Use MCP integrations** to reduce context switching
- **ALWAYS ASK FOR EXPLICIT REVIEW** before posting GitHub issues, PRs, or any external communications
- **STRICT SPEC COMPLIANCE**: When implementing any tool, spec, or app based on documentation, implement EXACTLY as specified - no additional files, no assumptions, no "helpful" extras beyond what's documented

## Memory System References

### Technology Stack Modules
Use when working with specific technologies:
- **Python Development:** `~/.claude/memories/stacks/python.md` (uv, ruff, pytest patterns)
- **Node.js Development:** `~/.claude/memories/stacks/nodejs.md` (pnpm, TypeScript, testing)
- **Frontend Development:** `~/.claude/memories/stacks/web-frontend.md` (React, Vite, Tailwind)

### MCP Integration References
Use when setting up or troubleshooting integrations:
- **Installation Guide:** `~/.claude/memories/mcp/installation.md`
- **GitHub Integration:** `~/.claude/memories/mcp/github-integration.md`
- **Hugging Face Integration:** `~/.claude/memories/mcp/huggingface-integration.md`

### Development Workflows
Reference for complex development methodologies:
- **Discovery-First:** For complex features or unfamiliar codebases
- **Test-Driven:** For well-defined functionality with clear requirements  
- **Visual Feedback:** For UI/UX development or visual outputs

### Quick Access Commands
```bash
# Memory system
python3 ~/.claude/memories/templates/generator.py /path/to/project
```

## Claude Code Focus Areas
Dotfiles management, command execution, file operations, git workflows, project analysis

---

*Lean context for immediate workflow enforcement. Reference detailed modules when needed for specific technology work.*