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

### GIT OPERATIONS FOR DOTFILES:
**Golden Rule:** Always use `chezmoi git -- <command>`, never raw `git` in HOME.

Examples:
- `chezmoi git -- status` (not `git status`)
- `chezmoi git -- rebase -i HEAD~3` (not `git rebase -i`)
- `chezmoi git -- push` (not `git push`)
- `chezmoi git -- commit -m "msg"` (not `git commit`)
- Edit in HOME → `chezmoi add` (not `git add`)


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
**Claude Config:** Direct chezmoi management via `dot_claude/` directory
**Git:** SSH commit signing enforced

### Code Standards
- 2-space indentation for shell scripts
- Comment non-obvious configuration choices
- Group related settings with clear headers
- Never commit secrets or credentials

### Workflow Principles
- **PROACTIVE AGENT DELEGATION**: Before starting non-trivial tasks, check `~/.claude/agents/` for specialists. Run `ls ~/.claude/agents/` and read relevant agent descriptions to understand capabilities. Delegate when an agent matches the task domain.
- **HOME → Source workflow**: Always edit files in HOME directory first, then `chezmoi add`
- **Verify success**: When using source → HOME workflow, verify `chezmoi apply` succeeds
- **Ask before creating** new tools/scripts - prefer enhancing existing ones
- **Test everything** before suggesting commands
- **Leverage Superpowers skills** for TDD, brainstorming, planning, and execution workflows
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
- **Verification-Driven:** Implementation verification from user perspective

Note: All workflows enhanced with Superpowers skill integration for rigorous execution patterns.

### Quick Access Commands
```bash
# Memory system
python3 ~/.claude/memories/templates/generator.py /path/to/project
```

## Claude Code Configuration Architecture

### Direct Chezmoi Management
**Claude configuration is now directly managed by chezmoi as `~/.local/share/chezmoi/dot_claude/`**

**Structure:**
```
~/.claude/                    # Runtime directory (managed by chezmoi)
├── agents/         (19)      # Specialized agents by category
├── hooks/          (9)       # Python workflow automation hooks
├── memories/       (30+)     # Project context & methodologies (42% token reduction via Superpowers)
├── commands/       (13)      # Custom slash commands
├── output-styles/  (8)       # Response formatting styles
├── status_lines/   (4)       # Status bar configurations
└── settings.json             # Global configuration

Local runtime data (NOT managed):
├── data/                     # Session data
├── projects/                 # Project configurations
├── todos/                    # Task management
├── settings.local.json       # Machine-specific overrides
└── shell-snapshots/          # Command history
```

### Agent Ecosystem (12 Active Agents)

**Core Operations (4)**
- `repo.md` - Git + GitHub operations via `gh` CLI (commits, PRs, issues, search)
- `system-environment.md` - System & package management (Homebrew, uv, npm)
- `dotfiles-manager.md` - Chezmoi dotfiles management (HOME→Source workflow)
- `agent-designer.md` - Creates new agents with doc discovery

**Platform Integrations (2)**
- `google-workspace.md` - Gmail, Calendar, Drive via `gog` CLI
- `executive-assistant.md` - Daily productivity rituals, calendar orchestration

**Content Creation (3)**
- `report-generator.md` - Reports with citations and references
- `document-writer.md` - Professional consulting documents
- `presentation-creator.md` - Quarto RevealJS presentations

**Development & Workflow (2)**
- `workflow-manager.md` - Workflow design & orchestration
- `ai-modeling-developer.md` - ML development with TDD enforcement

**Utility (1)**
- `hello-world.md` - Simple greeting

**Design Principles:**
- Agents encapsulate **workflows**, not thin tool wrappers
- Use CLI tools (`gh`, `gog`, `hf`) instead of MCP for context efficiency
- Dynamic discovery: check `~/.claude/agents/` before delegating

### Configuration Management
- **Source:** `~/.local/share/chezmoi/dot_claude/`
- **Runtime:** `~/.claude/` (automatically populated by chezmoi)
- **Local Data:** Excluded via `.chezmoiignore` (never version controlled)
- **Updates:** Edit source via chezmoi, then `chezmoi apply`

## Superpowers Plugin Integration

**Adoption Date:** October 2024
**Architecture:** Progressive Enhancement Pattern

### Division of Responsibility
- **Claude Memories:** Strategic patterns, when-to-use criteria, environment-specific tools
- **Superpowers Skills:** Tactical execution, rigid process discipline, bulletproof checklists
- **Integration:** Graceful degradation - Claude works standalone, enhances with Superpowers

### Key Skills Integrated
- `testing/test-driven-development/SKILL.md` - Strict RED-GREEN-REFACTOR TDD
- `collaboration/brainstorming/SKILL.md` - Interactive idea refinement
- `collaboration/writing-plans/SKILL.md` - Bite-sized task planning
- `collaboration/executing-plans/SKILL.md` - Batch execution with checkpoints
- `collaboration/subagent-driven-development/SKILL.md` - Task-by-task with code review

### Workflow Memory Updates
All workflow memories updated with Superpowers skill references:
- `test-driven.md`: Delegates detailed TDD execution to Superpowers
- `discovery-first.md`: References brainstorming & planning skills
- `verification-driven.md`: Integrated verification checklists
- `core-workflows.md`: Complete skill integration mapping

**Token Efficiency:** 42% reduction in workflow memories (818 lines saved) through strategic Superpowers delegation while preserving unique Claude Code patterns (uv, chezmoi, rg, fd, eza, delta).

## Claude Code Focus Areas
Dotfiles management, command execution, file operations, git workflows, project analysis, comprehensive report generation, agent ecosystem coordination

---

*Lean context for immediate workflow enforcement. Reference detailed modules when needed for specific technology work.*