# Agent Delegation Patterns

## Core Principle
**PROACTIVELY delegate to specialized agents** - they have domain expertise and dedicated tools. The main agent should orchestrate, not do everything directly.

## Delegation Decision Tree

```
User Request
    │
    ├─ Google Workspace (email, calendar, drive, docs)?
    │   └─► google-workspace agent
    │
    ├─ Git/GitHub operations (commits, PRs, issues)?
    │   └─► repo agent (comprehensive) or github-platform agent (GitHub-specific)
    │
    ├─ Dotfiles/chezmoi management?
    │   └─► dotfiles-manager agent
    │
    ├─ Create/modify agents?
    │   └─► agent-designer agent
    │
    ├─ Research from Confluence/Atlassian?
    │   └─► confluence-research agent
    │
    ├─ Multi-source client research?
    │   └─► client-research-coordinator agent
    │
    ├─ Morning brief/productivity ritual?
    │   └─► executive-assistant agent
    │
    ├─ Professional document creation?
    │   └─► document-writer agent
    │
    ├─ Report with citations?
    │   └─► report-generator agent
    │
    ├─ Presentation/slides?
    │   └─► presentation-creator agent
    │
    ├─ PR preparation/review?
    │   └─► pr-review-assistant agent
    │
    ├─ HuggingFace models/datasets?
    │   └─► huggingface-hub agent
    │
    ├─ AI/ML research news?
    │   └─► llm-research agent
    │
    ├─ System/environment setup?
    │   └─► system-environment agent
    │
    ├─ Workflow design/orchestration?
    │   └─► workflow-manager agent
    │
    └─ Work completion summary (TTS)?
        └─► work-completion-summary agent
```

## Trigger Keywords by Agent

| Agent | Trigger Keywords |
|-------|------------------|
| google-workspace | gmail, calendar, drive, docs, sheets, email, schedule, meeting |
| repo | git, commit, branch, merge, PR, pull request, push, repository |
| dotfiles-manager | dotfiles, chezmoi, config, .zshrc, HOME→Source |
| agent-designer | create agent, new agent, agent design |
| executive-assistant | morning brief, schedule, productivity, daily ritual |
| confluence-research | confluence, wiki, company docs, internal documentation |
| document-writer | professional document, consulting report, formal writing |
| report-generator | report, analysis, market research, citations, references |
| presentation-creator | slides, presentation, deck, Quarto, RevealJS |

## When NOT to Delegate

- Simple file reads/edits (use Read/Edit directly)
- Quick searches in known locations (use Glob/Grep)
- Single bash commands (use Bash directly)
- Conversations/explanations (respond directly)

## Delegation Syntax

```
Task: <agent-name> agent
"<clear, specific request with context>"
```

Example:
```
Task: google-workspace agent
"Search Gmail for emails from IDG in the last week, summarize key action items"
```

## Benefits of Delegation

1. **Context isolation** - Agent handles verbose operations, returns clean summary
2. **Domain expertise** - Agents have specialized knowledge and tool access
3. **Parallel execution** - Multiple agents can run concurrently
4. **Token efficiency** - Heavy processing stays in agent context
