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
- **Descriptive Commits:** Explain "why" not just "what" in commit messages
- **Continuous Validation:** Test assumptions early and often
- **Always Include Links:** When referencing GitHub issues, documentation, or external resources, ALWAYS provide clickable links

## Integration Points
- Task management via Jira integration
- Version control following git conventions
- Tool preferences from essential-tools module