# Core Development Workflows

This module coordinates the primary development methodologies and imports specific workflow patterns.

## Workflow Import Chain
@discovery-first.md
@test-driven.md
@visual-feedback.md
@verification-driven.md

## Workflow Selection Criteria

### Discovery-First Development
**When:** Complex features or unfamiliar codebases where requirements aren't fully clear
**Trigger:** High uncertainty, new technology, large refactoring

### Test-Driven Workflow  
**When:** Adding new functionality with clear requirements
**Trigger:** Well-defined features, API development, critical business logic

### Visual Feedback Loop
**When:** UI/UX development or visual outputs
**Trigger:** Frontend work, data visualization, design implementation

## Universal Workflow Principles

- **TodoWrite Planning:** Always create implementation plan before coding
- **User Confirmation:** Present complex plans for approval before implementation
- **🔍 MANDATORY VERIFICATION:** Every implementation MUST include verification from user perspective
- **🤖 AGENT-FIRST ROUTING:** Use specialized agents (repository-manager, dotfiles-manager, research agents) instead of basic tools
- **🔗 ALWAYS HYPERLINK EVERY REFERENCE:** Any library, study, dataset, tool, or resource mentioned must be hyperlinked
- **📋 NO PRINT STATEMENTS:** In notebook cells, use tables/plots/DataFrames only, never print statements
- **✅ VERIFY BEFORE CLAIMING:** WebFetch technical details and quote sources directly before making any claims
- **Descriptive Commits:** Explain "why" not just "what" in commit messages
- **Continuous Validation:** Test assumptions early and often

## Integration Points
- Task management via Jira integration
- Version control following git conventions
- Tool preferences from essential-tools module

## 🔗 Superpowers Skills Integration

The workflow memories provide high-level patterns and decision frameworks. For detailed execution and strict process enforcement, delegate to Superpowers skills:

### Workflow → Skills Mapping

| Claude Memory Workflow | Superpowers Skill | When to Use Skill |
|------------------------|-------------------|-------------------|
| test-driven.md | `${SUPERPOWERS_SKILLS_ROOT}/skills/testing/test-driven-development/SKILL.md` | For strict RED-GREEN-REFACTOR TDD with checklist enforcement |
| discovery-first.md | `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/brainstorming/SKILL.md` | When refining ideas into designs (40% overlap, different phases) |
| - | `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/writing-plans/SKILL.md` | After brainstorming, for bite-sized task planning |
| - | `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` | Batch execution of plans with review checkpoints |
| - | `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/subagent-driven-development/SKILL.md` | Task-by-task execution with code review between steps |

### Unique to Claude Memories (No Skill Equivalent)
- **verification-driven.md**: Verification from user perspective (no Superpowers skill)
- **visual-feedback.md**: Visual iteration workflow (no Superpowers skill)

### Division of Responsibility
- **Memories**: Strategic patterns, when to use what approach, high-level workflows
- **Skills**: Tactical execution, rigid process discipline, bulletproof checklists

**Best Practice**: Reference the relevant Superpowers skill when detailed execution discipline is needed.