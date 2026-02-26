# Agent Ecosystem

> **Comprehensive guide to Claude Code's 12 specialized agents**

## Quick Reference

| Agent | Category | Use When | Keywords |
|-------|----------|----------|----------|
| `repo` | Core | Git operations, commits, PRs | "commit", "PR", "branch", "merge" |
| `system-environment` | Core | Package installation, environment setup | "install", "homebrew", "uv", "setup" |
| `dotfiles-manager` | Core | Chezmoi dotfiles management | "dotfiles", "chezmoi", "config files" |
| `agent-designer` | Core | Agent design, ecosystem analysis | "create agent", "agent design" |
| `google-workspace` | Platform | Gmail, Drive, Docs, Calendar access | "email", "calendar", "google doc" |
| `executive-assistant` | Platform | Calendar orchestration, email triage | "morning brief", "schedule", "triage" |
| `report-generator` | Content | Cited reports, market analyses | "report", "analysis", "market research" |
| `document-writer` | Content | Formal documents, consulting output | "professional document", "formal writing" |
| `presentation-creator` | Content | Quarto RevealJS slide decks | "presentation", "slides", "deck" |
| `workflow-manager` | Development | Workflow design, multi-agent orchestration | "workflow", "process", "multi-step" |
| `ai-modeling-developer` | Development | ML development with TDD | "model", "ML", "training", "dataset" |
| `hello-world` | Utility | Simple greetings | "hi claude", "hello" |

---

## Understanding Agents vs Skills vs Commands

### Agents (Subagents)
**Model-invoked or user-invoked** - Separate AI instances with their own context, tools, and configuration.

**When to use:**
- Complex multi-step tasks
- Tasks requiring isolated context
- Specialized tool access
- Long-running operations
- Resumable tasks

**Example:** A 50-file code review runs better in a separate context.

### Skills
**Model-invoked only** - Claude discovers and applies them automatically based on description.

**When to use:**
- Multi-step workflows
- Domain expertise applied automatically
- Capabilities requiring scripts or templates
- Team standardization

**Example:** PDF processing with extraction scripts.

### Commands (Slash Commands)
**User-invoked only** - An explicit `/command` triggers a predefined prompt.

**When to use:**
- Frequent simple prompts
- Quick reminders or templates
- Workflows requiring explicit control

**Example:** `/commit` for git commit guidance.

### Decision Framework

```
Is it complex AND multi-file? → Skill
Is it simple AND frequently used? → Command
Does it need isolated context? → Agent
Do you want automatic use? → Skill
Do you want explicit control? → Command or Agent
```

---

## Agent Categories

### Core Operations (4 agents)

**`repo`** - Comprehensive repository management
- Git workflows, commits, branches
- GitHub/GitLab operations (issues, PRs)
- SSH signing, conventional commits
- Multi-platform repository coordination
- **Tools:** Read, Write, Edit, Bash, Glob, Grep, GitHub MCP tools

**`system-environment`** - System and package management
- Homebrew, uv, npm installation
- Development environment setup
- System configuration (macOS settings, PATH)
- Tool installation and updates
- **Tools:** Bash, Read, Write, WebFetch
- **Not for:** Dotfiles (use dotfiles-manager)

**`dotfiles-manager`** - Chezmoi dotfiles repository
- HOME→Source workflow enforcement
- Configuration file deployment
- Documentation synchronization
- **Critical:** Always use `chezmoi git --`, never raw `git`
- **Tools:** Bash, Read, Write, Edit, chezmoi, rg, fd, eza, bat, delta
- **Not for:** Package installation (use system-environment)

**`agent-designer`** - Agent ecosystem architect
- Design new agents
- Analyze agent gaps and overlaps
- Agent coordination patterns
- **Tools:** All tools

### Platform Integrations (2 agents)

**`google-workspace`** - Google productivity suite
- Gmail, Drive, Docs, Calendar, Sheets
- Email management, document creation
- Calendar scheduling
- **Tools:** Google Workspace MCP tools

**`executive-assistant`** - Executive assistant
- Calendar orchestration
- Email triage and communications
- Task coordination
- Daily productivity rituals
- **Tools:** Google Workspace MCP, Atlassian MCP, TodoWrite

### Content & Research (3 agents)

**`report-generator`** - Professional reports with citations
- Market analyses, strategic documents
- **Mandatory:** All claims require sources
- TAM calculations, competitive intelligence
- **Tools:** WebSearch, WebFetch, Read, Write

**`document-writer`** - Formal document creation
- Professional reports, consulting documents
- Proper formatting and citation standards
- Academic writing quality
- **Tools:** Read, Write, MultiEdit, Task

**`presentation-creator`** - Executive presentations
- Quarto RevealJS presentations
- One-slide-one-idea principle
- Modern aesthetics, visual hierarchy
- Creative design with superior composition
- **Tools:** Read, Write, WebFetch, Task, Quarto

### Development & Workflow (2 agents)

**`workflow-manager`** - Workflow design and orchestration
- Workflow documentation creation
- Multi-agent execution coordination
- Glow presentation of process docs
- **Tools:** Task, Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebFetch, glow

**`ai-modeling-developer`** - ML development with TDD
- Test-strategy-first workflows
- Parallel test/code development
- Empirical research integration
- Statistical simulations, data pipelines
- **Tools:** Read, Write, Grep, Glob, WebFetch

### Utility (1 agent)

**`hello-world`** - Simple greeting agent
- Responds to greetings with friendly messages
- **Tools:** WebSearch

---

## Auto-Invocation Patterns

### Why Agents Fail to Auto-Invoke

**Problem:** Many agents fire only when explicitly requested.

**Root causes:**
1. **Vague descriptions** - No clear "when to use" statements
2. **Missing keywords** - No specific trigger phrases
3. **No proactive invitation** - No "Use proactively when..." language

### Best Practices for Auto-Invocation

**Strong pattern:**
```yaml
description: Use proactively for [specific task]. Keywords: "keyword1", "keyword2", "keyword3". Use when user mentions [scenario].
```

**Examples:**

✅ **Good (report-generator):**
```yaml
description: Use proactively for generating professional consulting reports, market analyses, and strategic documents with MANDATORY citations and references. Keywords include "report", "analysis", "market research", "consulting document", "strategic assessment", "TAM calculation", "competitive intelligence", or "professional documentation". ALL claims require sources. NO unsourced statistics allowed.
```

❌ **Poor (agent-designer - needs improvement):**
```yaml
description: Intelligent agent architect that ultrathinks agent design decisions using deep reasoning capabilities.
```

**Improvement needed:**
```yaml
description: Use proactively when designing new agents, analyzing agent ecosystem gaps, or coordinating agent workflows. Keywords include "create agent", "new agent", "agent design", "agent architecture", "workflow automation", "agent coordination".
```

### Keyword Density Matters

**High-performing agents** include 8-12 specific keywords in their description.
**Low-performing agents** include 2-3 generic keywords.

---

## Modern CLI Tooling Standards

All agents should use modern CLI tools:

| Legacy | Modern | Use Case |
|--------|--------|----------|
| `ls` | `eza` | Directory listings with git integration |
| `grep` | `rg` (ripgrep) | Fast content search, respects .gitignore |
| `find` | `fd` | File search with simpler syntax |
| `cat` | `bat` | Syntax highlighting for file viewing |
| `diff` | `delta` | Enhanced git diffs |
| `top` | `btop` | Interactive system monitor |

### Current Issues

**`agent-designer`** - Still uses legacy tools (HIGH PRIORITY FIX):
```bash
# Current (WRONG)
ls ~/.claude/agents/*.md | head -10
grep -h "^description:" ~/.claude/agents/*.md

# Should be
fd "\.md$" ~/.claude/agents/
rg "^description:" ~/.claude/agents/
```

**All other agents** - Generally good, but should explicitly mention modern tools in descriptions.

---

## Naming Conventions

### Naming Evolution

**Standardized Pattern:** `domain-noun` or `verb-noun`

**Recent Improvements (2025-12-26):**
- `document-architect` → `document-writer` (action-oriented)
- `slide-architect` → `presentation-creator` (clearer purpose)
- `meta` → `agent-designer` (describes function)
- `atlas-exec` → `executive-assistant` (role clarity)

**Current Patterns:**
- Verb-noun: `report-generator`, `presentation-creator`, `document-writer`
- Domain-specialist: `dotfiles-manager`, `system-environment`, `agent-designer`

**Rationale:**
- Action-oriented over role-oriented
- Clear function over clever names
- Consistent pattern aids discoverability

---

## Agent Interaction Patterns

### Coordination

Agents can invoke other agents via the `Task` tool:
```python
Task(subagent_type="repo", prompt="Create PR for feature branch")
```

### Hand-offs

Common patterns:
- `system-environment` → `dotfiles-manager` (install tools, then configure)
- `workflow-manager` → specialized agents (design workflow, then execute)
- `agent-designer` → specialized agents (design new agent, then implement)

### Parallel Execution

Multiple agents can run simultaneously:
```python
# Single message with multiple Task calls
Task(subagent_type="report-generator", ...)
Task(subagent_type="document-writer", ...)
```

---

## Maintenance

### Add a New Agent

1. Design the agent with `agent-designer`
2. Consider whether a Skill or Command fits better
3. Write a clear description with "Use proactively when..." and keywords
4. Grant only the tools the agent needs (least privilege)
5. Follow modern CLI tooling standards
6. Test auto-invocation before deploying
7. Update this documentation

### Update an Existing Agent

1. Edit the agent file in `~/.claude/agents/`
2. Test changes in a conversation
3. Update this documentation if behavior changes
4. Version-control via dotfiles-manager

### Deprecate an Agent

1. Identify redundant or unused agents
2. Archive to `~/.claude/agents/archived/`
3. Update routing rules in `mandatory-checks.md`
4. Update this documentation

---

## Common Pitfalls

### Creating Agents for Everything

**Problem:** Too many narrow agents hinder discovery.

**Solution:** Use Skills for specialized knowledge, Agents for context isolation.

### Unclear Descriptions

**Problem:** Generic descriptions prevent auto-invocation.

**Solution:** Add dense keywords, clear "Use when..." statements, and proactive invitations.

### Tool Overload

**Problem:** Every agent receives all tools.

**Solution:** Grant only the tools each agent needs.

### Ignoring Modern Tooling

**Problem:** Agents use legacy `grep`/`find` when `rg`/`fd` exist.

**Solution:** Follow the modern CLI tooling standards above.

---

## Future Improvements

### Planned Enhancements

1. **Agent routing rules** - Update `mandatory-checks.md` with current agent names
2. **Auto-invocation testing** - Verify keyword triggers work
3. **Modern tooling audit** - Ensure all agents use rg/fd/eza/bat where appropriate
4. **Naming standardization** - Apply consistent verb-noun pattern
5. **Skills migration** - Move appropriate agents to Skills
6. **Documentation automation** - Auto-generate this from agent metadata

### Metrics to Track

- Agent invocation frequency (auto vs manual)
- Agent success rate (task completion)
- Tool usage patterns (modern vs legacy)
- Description effectiveness (keyword density vs invocation rate)

---

## References

- [Agent design patterns](~/.claude/agents/)
- [Workflow coordination](~/.claude/memories/workflows/)
- [Modern CLI tools](~/.docs/tool-reference.md)
- [Routing rules](~/.claude/memories/private_core-behavior/mandatory-checks.md)

---

**Last Updated:** 2026-02-25
**Maintainer:** dotfiles-manager agent
**Source:** ~/.docs/private_agents.md (managed by chezmoi)
