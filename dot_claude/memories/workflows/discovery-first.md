# Discovery-First Development Workflow

## Purpose and Scope
For complex features or unfamiliar codebases where requirements aren't fully clear and exploration is needed.

## 🔗 Superpowers Skills Integration

For structured refinement after exploration:
- **Brainstorming:** `brainstorming` skill (Superpowers plugin)
- **Writing Plans:** `writing-plans` skill (Superpowers plugin)

## When to Use
- Complex features with unclear requirements
- Unfamiliar codebases
- Large refactoring projects
- New technology exploration
- Legacy system modifications

## Process Flow

**Explore → Plan → Confirm → Code → Commit**

1. **Explore:** Use search tools (rg, fd) to understand codebase, map architecture, identify dependencies
2. **Plan:** Create TodoWrite plan, break down tasks, identify risks
3. **Confirm:** Present plan for user approval, adjust based on feedback
4. **Code:** Implement following approved plan, validate assumptions
5. **Commit:** Descriptive messages explaining "why", reference discovery process

## Tool Integration

```bash
# Codebase exploration
rg "pattern" --type=language
eza -la --tree
bat filename
```

### Documentation as You Go
- Update architecture notes in real-time
- Document surprising discoveries
- Note refactoring opportunities
- Record performance/security considerations

## Success Criteria
- ✅ Clear system understanding before coding
- ✅ User approval on approach
- ✅ Comprehensive plan with dependencies
- ✅ Documented decisions

## Common Pitfalls
- ❌ Starting to code without sufficient exploration
- ❌ Skipping user confirmation
- ❌ Inadequate documentation
- ❌ Over-engineering

## Integration with Other Workflows
- Transitions to Test-Driven once requirements clear
- Often combined with Visual Feedback for UI-heavy discovery
