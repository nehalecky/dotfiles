# Discovery-First Development Workflow

## Purpose and Scope
For complex features or unfamiliar codebases where requirements aren't fully clear and exploration is needed.

## When to Use
- Complex features with unclear requirements
- Working with unfamiliar codebases  
- Large refactoring projects
- New technology exploration
- Legacy system modifications

## Process Flow

### 1. Explore Phase
- **Use search tools extensively** to understand the codebase
- **Map system architecture** and identify key components
- **Document findings** as you discover them
- **Identify dependencies** and potential impact areas

### 2. Plan Phase  
- **Create TodoWrite plan** before implementation
- **Break down complex tasks** into manageable steps
- **Identify risks and unknowns** that need validation
- **Estimate effort** based on exploration findings

### 3. Confirm Phase
- **Present plan to user** for approval
- **Discuss approach** and get feedback on strategy
- **Adjust plan** based on user input
- **Get explicit approval** before proceeding

### 4. Code Phase
- **Implement with confidence** following approved plan
- **Validate assumptions** as you build
- **Document decisions** that differ from plan
- **Commit incremental progress** regularly

### 5. Commit Phase
- **Descriptive commit messages** explaining "why" not just "what"
- **Reference discovery process** in commit description
- **Include lessons learned** for future developers

## Tool Integration Patterns

### Search and Analysis
```bash
# Use preferred tools for codebase exploration
rg "pattern" --type=language    # ripgrep for code search
eza -la --tree                  # directory structure analysis
bat filename                    # syntax-highlighted file viewing
```

### Documentation as You Go
- Update architecture notes in real-time
- Document surprising discoveries
- Note potential refactoring opportunities
- Record performance or security considerations

## Success Criteria
- ✅ **Clear understanding** of system architecture before coding
- ✅ **User approval** on implementation approach  
- ✅ **Comprehensive plan** with identified dependencies
- ✅ **Documented decisions** for future reference
- ✅ **Working implementation** that meets requirements

## Common Pitfalls to Avoid
- ❌ **Starting to code** without sufficient exploration
- ❌ **Skipping user confirmation** on complex approaches
- ❌ **Inadequate documentation** of discovery process
- ❌ **Over-engineering** based on incomplete understanding

## Integration with Other Workflows
- May transition to **Test-Driven** workflow once requirements are clear
- Often combined with **Visual Feedback** for UI-heavy discovery
- Always incorporates standard **Git Conventions** for commits