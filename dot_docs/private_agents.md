# Agent Ecosystem

> **Comprehensive guide to Claude Code's 19 specialized agents**

## Quick Reference

| Agent | Category | Use When | Keywords |
|-------|----------|----------|----------|
| `repo` | Core | Repository operations (git, commits, PRs) | "commit", "PR", "branch", "merge" |
| `system-environment` | Core | Package installation, env setup | "install", "homebrew", "uv", "setup" |
| `dotfiles-manager` | Core | Chezmoi dotfiles management | "dotfiles", "chezmoi", "config files" |
| `agent-designer` | Core | Agent design and ecosystem | "create agent", "agent design" |
| `github-platform` | Platform | GitHub Actions, Discussions, Projects | "github actions", "workflow", "discussion" |
| `google-workspace` | Platform | Gmail, Drive, Docs, Calendar | "email", "calendar", "google doc" |
| `executive-assistant` | Platform | Executive calendar/email mgmt | "morning brief", "schedule", "triage" |
| `huggingface-hub` | Platform | ML model search and download | "huggingface", "model", "whisper", "llama" |
| `report-generator` | Content | Professional reports with citations | "report", "analysis", "market research" |
| `document-writer` | Content | Formal documents, citations | "professional document", "formal writing" |
| `presentation-creator` | Content | Quarto/RevealJS presentations | "presentation", "slides", "deck" |
| `client-research-coordinator` | Content | Multi-platform research | "client research", "comprehensive study" |
| `confluence-research` | Content | Confluence knowledge base | "confluence", "documentation search" |
| `workflow-manager` | Development | Workflow design & orchestration | "workflow", "process", "multi-step" |
| `ai-modeling-developer` | Development | ML development with TDD | "model", "ML", "training", "dataset" |
| `pr-review-assistant` | Development | Code review preparation | "PR prep", "review", "commit analysis" |
| `llm-research` | Development | AI/ML news and developments | "AI news", "LLM research", "latest models" |
| `work-completion-summary` | Development | TTS audio summaries | "tts", "audio summary", "completion" |
| `hello-world` | Utility | Simple greetings | "hi claude", "hello" |

---

## Understanding Agents vs Skills vs Commands

### Agents (Subagents)
**Model-invoked OR user-invoked** - Separate AI instances with own context, tools, and configuration.

**When to use:**
- Complex multi-step tasks
- Need isolated context (won't pollute main conversation)
- Specialized tool access requirements
- Long-running operations
- Resumable tasks

**Example:** Code review that analyzes 50 files - better in separate context.

### Skills
**Model-invoked only** - Claude autonomously discovers and uses based on description.

**When to use:**
- Complex workflows requiring multiple steps
- Domain expertise you want applied automatically
- Capabilities requiring scripts/templates
- Team standardization

**Example:** PDF processing with extraction scripts.

### Commands (Slash Commands)
**User-invoked only** - Explicit `/command` triggers predefined prompt.

**When to use:**
- Frequently-used simple prompts
- Quick reminders or templates
- Workflows you want explicit control over

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
- **NOT for:** Dotfiles (use dotfiles-manager)

**`dotfiles-manager`** - Chezmoi dotfiles repository
- HOME→Source workflow enforcement
- Configuration file deployment
- Documentation synchronization
- **⚠️ CRITICAL:** Always use `chezmoi git --`, never raw `git`
- **Tools:** Bash, Read, Write, Edit, chezmoi, rg, fd, eza, bat, delta
- **NOT for:** Package installation (use system-environment)

**`meta`** - Agent ecosystem architect
- Design new agents
- Analyze agent gaps and overlaps
- Agent coordination patterns
- **Tools:** All tools
- **⚠️ NOTE:** Currently uses legacy `ls`/`grep` - needs modernization to `fd`/`rg`

### Platform Integrations (4 agents)

**`github-platform`** - GitHub-specific features
- GitHub Actions, Workflows
- Discussions, Projects
- Platform-specific operations
- **NOT for:** Basic repo ops (use `repo`)
- **Tools:** GitHub MCP tools

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

**`huggingface-hub`** - ML model gateway
- Search and download models/datasets
- HuggingFace Hub integration
- Model cache management
- **Tools:** Bash, WebFetch, HuggingFace MCP tools

### Content & Research (5 agents)

**`report-generator`** - Professional reports with citations
- Market analyses, strategic documents
- **MANDATORY:** All claims require sources
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

**`client-research-coordinator`** - Multi-platform research
- Comprehensive client research
- Spans Confluence, GitHub, Google Workspace
- Consultancy deliverable preparation
- **Tools:** Atlassian MCP, GitHub MCP, Google Workspace MCP, HuggingFace MCP

**`confluence-research`** - Confluence knowledge base
- Research and content retrieval
- Product vision, company documentation
- CQL search capabilities
- **Tools:** Atlassian MCP (Confluence-specific)

### Development & Workflow (5 agents)

**`workflow-manager`** - Unified workflow design & orchestration
- Designs workflows (creates documentation)
- Orchestrates workflows (coordinates multi-agent execution)
- Glow presentation of process docs
- **Tools:** Task, Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebFetch, glow

**`ai-modeling-developer`** - ML development with TDD
- Test-strategy-first workflows
- Parallel test/code development
- Empirical research integration
- Statistical simulations, data pipelines
- **Tools:** Read, Write, Grep, Glob, WebFetch

**`pr-review-assistant`** - Code review preparation
- Analyzes commits for review
- Organizes logical PRs
- Generates comprehensive descriptions
- Interactive review support
- **Tools:** Read, Grep, Glob, Bash, WebFetch, GitHub MCP

**`llm-research`** - AI/ML news and developments
- Latest LLM news and innovations
- Actionable insights for engineering
- New tool and technique discovery
- **Tools:** Bash, Firecrawl MCP, WebFetch

**`work-completion-summary`** - TTS audio summaries
- Concise audio summaries of completed work
- Suggests next steps
- **Triggered:** When work completes or user says "tts"
- **Tools:** Bash, ElevenLabs MCP

### Utility (1 agent)

**`hello-world`** - Simple greeting agent
- Responds to greetings with friendly messages
- **Tools:** WebSearch

---

## Auto-Invocation Patterns

### Why Agents Aren't Being Used Automatically

**Problem:** Many agents are only invoked when explicitly requested.

**Root causes:**
1. **Vague descriptions** - No clear "when to use" statements
2. **Missing keywords** - Lack of specific trigger phrases
3. **No proactive invitation** - Missing "Use proactively when..." language

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

❌ **Poor (meta - current):**
```yaml
description: Intelligent agent architect that ultrathinks agent design decisions using deep reasoning capabilities.
```

**Improvement needed:**
```yaml
description: Use proactively when designing new agents, analyzing agent ecosystem gaps, or coordinating agent workflows. Keywords include "create agent", "new agent", "agent design", "agent architecture", "workflow automation", "agent coordination".
```

### Keyword Density Matters

**High-performing agents** have 8-12 specific keywords in description.
**Low-performing agents** have 2-3 generic keywords.

---

## Modern CLI Tooling Standards

All agents should use modern CLI tools where appropriate:

| Legacy | Modern | Use Case |
|--------|--------|----------|
| `ls` | `eza` | Directory listings with git integration |
| `grep` | `rg` (ripgrep) | Fast content search, respects .gitignore |
| `find` | `fd` | File search with simpler syntax |
| `cat` | `bat` | Syntax highlighting for file viewing |
| `diff` | `delta` | Enhanced git diffs |
| `top` | `btop` | Interactive system monitor |

### Current Issues

**`meta.md`** - Uses legacy tools (HIGH PRIORITY FIX):
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
- Tool-focused: `huggingface-hub`, `github-platform`

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
- `client-research-coordinator` → research agents (orchestrate multi-source)

### Parallel Execution

Multiple agents can run simultaneously:
```python
# Single message with multiple Task calls
Task(subagent_type="github-platform", ...)
Task(subagent_type="confluence-research", ...)
```

---

## Maintenance

### Adding New Agents

1. Use `meta` agent to design new agent
2. Consider if it should be a Skill or Command instead
3. Write clear description with "Use proactively when..." and keywords
4. Grant appropriate tools (principle of least privilege)
5. Use modern CLI tooling standards
6. Test auto-invocation before deploying
7. Update this documentation

### Updating Agents

1. Edit agent file in `~/.claude/agents/`
2. Test changes in conversation
3. Update this documentation if behavior changes
4. Use dotfiles-manager for version control

### Deprecating Agents

1. Identify redundant or unused agents
2. Archive to `~/.claude/agents/archived/`
3. Update routing rules in `mandatory-checks.md`
4. Update this documentation

---

## Common Pitfalls

### ❌ Creating Agents for Everything

**Problem:** Too many narrow agents creates discovery issues.

**Solution:** Use Skills for specialized knowledge, Agents for context isolation.

### ❌ Unclear Descriptions

**Problem:** Generic descriptions prevent auto-invocation.

**Solution:** Dense keywords, clear "Use when..." statements, proactive invitation.

### ❌ Tool Overload

**Problem:** Granting all tools to every agent.

**Solution:** Grant minimum tools needed for agent's function.

### ❌ Ignoring Modern Tooling

**Problem:** Using legacy `grep`/`find` when `rg`/`fd` available.

**Solution:** Follow modern CLI tooling standards above.

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

- [Agent design patterns](/Users/nehalecky/.claude/agents/)
- [Workflow coordination](/Users/nehalecky/.claude/memories/workflows/)
- [Modern CLI tools](/Users/nehalecky/.docs/tool-reference.md)
- [Routing rules](/Users/nehalecky/.claude/memories/core-behavior/mandatory-checks.md)

---

**Last Updated:** 2025-12-26
**Maintainer:** dotfiles-manager agent
**Source:** ~/.docs/agents.md (managed by chezmoi)
