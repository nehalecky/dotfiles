# Self-Review Workflow

A comprehensive workflow for thoughtful self-review of code changes using the pr-review-assistant agent.

## Purpose

Transform accumulated local commits into well-organized, thoroughly reviewed pull requests that maintain high code quality through structured self-review.

## Workflow Overview

```
Local Development (24 commits)
    ↓
PR Review Assistant Analysis
    ↓
Logical PR Organization
    ↓
Context Generation
    ↓
GitHub PR Creation
    ↓
Thoughtful Self-Review
    ↓
Merge Decision
```

## Detailed Process

### Phase 1: Development Accumulation
**Duration**: Days to weeks
**Output**: 24+ local commits ahead of origin

Normal development workflow where you:
- Make changes following conventional commits
- Test locally but don't push
- Continue until ready for batch review

### Phase 2: Review Preparation
**Duration**: 15-30 minutes
**Tool**: pr-review-assistant

```bash
# Invoke the review assistant
> Use pr-review-assistant to analyze my local changes

# Assistant will:
# 1. Analyze all commits ahead of origin
# 2. Categorize changes by type and risk
# 3. Suggest logical PR groupings
# 4. Generate review checklists
```

**Decision Point**: Accept suggested PR organization or request adjustments

### Phase 3: PR Creation
**Duration**: 10-15 minutes per PR
**Tools**: pr-review-assistant + repository-manager

For each PR group:
1. **Create feature branch**
   ```bash
   > Use repository-manager to create branch for [PR description]
   ```

2. **Cherry-pick relevant commits**
   ```bash
   git cherry-pick [commit-hash-1] [commit-hash-2] ...
   ```

3. **Generate PR description**
   ```bash
   > Use pr-review-assistant to generate PR description for this branch
   ```

4. **Create GitHub PR**
   ```bash
   > Use github-operations-agent to create PR with generated description
   ```

### Phase 4: Self-Review Process
**Duration**: 20-40 minutes per PR
**Platform**: GitHub PR interface

**Review Checklist**:
- [ ] **Purpose Clear**: Does PR description explain "why"?
- [ ] **Changes Logical**: Do all commits belong together?
- [ ] **Tests Adequate**: Is new functionality tested?
- [ ] **Docs Updated**: Are docs accurate for changes?
- [ ] **No Regressions**: Do existing tests still pass?
- [ ] **Performance OK**: No obvious performance issues?
- [ ] **Security Considered**: No security vulnerabilities introduced?

**Interactive Support**:
```bash
# During review, ask questions like:
> Use pr-review-assistant to explain changes in [file]
> Use pr-review-assistant to analyze test coverage for this PR
> Use pr-review-assistant to identify potential risks
```

### Phase 5: Review Iterations
**Duration**: Variable
**Actions**: Based on self-review findings

- **Minor Issues**: Fix directly in PR branch
- **Major Issues**: Close PR, reorganize, resubmit
- **Questions**: Use assistant for clarification
- **Documentation**: Update as needed

### Phase 6: Merge Decision
**Duration**: 5 minutes
**Criteria**: All review checks satisfied

Once satisfied with review:
1. Merge PR on GitHub
2. Pull changes locally
3. Continue with next PR or resume development

## Workflow Variations

### Quick Review Mode
For low-risk changes (docs, tests):
1. Single PR for all related changes
2. Simplified review checklist
3. Faster merge decision

### Detailed Review Mode
For high-risk changes (core logic, breaking changes):
1. Smaller, focused PRs
2. Comprehensive review checklist
3. Consider requesting peer review
4. Extended self-review period

### Emergency Mode
For critical fixes:
1. Single commit PR
2. Expedited review
3. Post-merge detailed review

## Integration Points

### With Existing Agents
- **repository-manager**: Branch and commit operations
- **github-operations-agent**: PR creation and management
- **workflow-designer**: Custom workflow documentation

### With Development Tools
- **Git**: Commit organization and cherry-picking
- **GitHub**: PR interface for review
- **Testing**: Local test execution before PR
- **CI/CD**: Automated checks on PR

## Best Practices

### Commit Organization
- Group related changes together
- Keep PRs under 400 lines when possible
- Separate high-risk from low-risk changes
- Maintain clear commit messages

### Review Quality
- Take breaks between reviewing PRs
- Use GitHub's review features (comments, suggestions)
- Actually read the code, don't just skim
- Test locally if uncertain about changes

### Documentation
- Update PR descriptions with review findings
- Document decisions made during review
- Link related issues and discussions
- Include examples or screenshots when helpful

## Common Patterns

### Pattern 1: Feature Development
```
feature commits (8-10) → single feature PR → detailed review
```

### Pattern 2: Bug Fix Batch
```
fix commits (5-6) → fixes PR → quick review with test focus
```

### Pattern 3: Documentation Update
```
docs commits (10-12) → docs PR → content accuracy review
```

### Pattern 4: Mixed Changes
```
24 mixed commits → 3-4 organized PRs → varied review depth
```

## Troubleshooting

### Too Many Conflicts
- Review PR organization strategy
- Consider smaller, sequential PRs
- Use rebase to resolve conflicts

### Unclear Changes
- Use pr-review-assistant for clarification
- Add more context to PR description
- Consider splitting complex changes

### Review Fatigue
- Take breaks between PRs
- Review high-risk changes when fresh
- Consider spreading review over multiple sessions

## Success Metrics

- ✅ All changes reviewed before merge
- ✅ PRs logically organized
- ✅ Review findings addressed
- ✅ No post-merge surprises
- ✅ Improved code quality over time

## Workflow Commands Summary

```bash
# Start review process
> Use pr-review-assistant to analyze my local changes

# Create PR with context
> Use pr-review-assistant to generate PR description
> Use github-operations-agent to create PR

# During review
> Use pr-review-assistant to explain [specific change]
> Use pr-review-assistant to analyze risks

# Post-review
> Use repository-manager to merge and sync
```

This workflow ensures thoughtful self-review while maintaining development velocity and code quality.