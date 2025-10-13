# Core Development Workflows

This module coordinates the primary development methodologies and imports specific workflow patterns.

## Workflow Import Chain
@discovery-first.md
@test-driven.md
@visual-feedback.md
@verification-driven.md

## Workflow Selection Criteria

**Discovery-First:** Complex features or unfamiliar codebases (high uncertainty)
**Test-Driven:** Adding functionality with clear requirements (well-defined)
**Visual Feedback:** UI/UX development or visual outputs (frontend work)

## Universal Workflow Principles

- **TodoWrite Planning:** Create implementation plan before coding
- **User Confirmation:** Present complex plans for approval
- **🔍 MANDATORY VERIFICATION:** Every implementation MUST verify from user perspective
- **🔗 ALWAYS HYPERLINK:** Every library, study, dataset, tool, or resource
- **✅ VERIFY BEFORE CLAIMING:** WebFetch technical details, quote sources directly
- **Descriptive Commits:** Explain "why" not just "what"
- **Continuous Validation:** Test assumptions early and often

## 🔗 Superpowers Skills Integration

Workflow memories provide high-level patterns. For detailed execution, delegate to Superpowers skills:

| Claude Memory | Superpowers Skill | When to Use |
|---------------|-------------------|-------------|
| test-driven.md | `testing/test-driven-development/SKILL.md` | Strict RED-GREEN-REFACTOR TDD |
| discovery-first.md | `collaboration/brainstorming/SKILL.md` | Refining ideas into designs |
| - | `collaboration/writing-plans/SKILL.md` | Bite-sized task planning |
| - | `collaboration/executing-plans/SKILL.md` | Batch execution with review |
| - | `collaboration/subagent-driven-development/SKILL.md` | Task-by-task with code review |

**Unique to Claude:** verification-driven.md, visual-feedback.md (no Superpowers equivalents)

**Division:** Memories = strategic patterns | Skills = tactical execution
