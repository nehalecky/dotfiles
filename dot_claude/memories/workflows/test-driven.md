# Test-Driven Development Workflow

## Purpose and Scope
For adding new functionality with clear requirements where the interface and expected behavior are well-understood.

## 🔗 Superpowers Skill Integration

**For strict RED-GREEN-REFACTOR TDD execution:**
`${SUPERPOWERS_SKILLS_ROOT}/skills/testing/test-driven-development/SKILL.md`

The Superpowers TDD skill provides rigid discipline, TodoWrite enforcement, and bulletproof process. Use it for detailed step-by-step TDD execution.

**This memory provides**: High-level TDD patterns and when to use TDD.
**Superpowers skill provides**: Strict execution discipline and detailed process.

## When to Use
- Adding new functionality with clear requirements
- API development with defined contracts
- Critical business logic requiring high confidence
- Well-understood features where test cases are obvious
- Library or utility function development
- Bug fixes where the desired behavior is clear

## Tool Integration Patterns

### Testing Framework Setup
```bash
# Python projects
uv add pytest pytest-cov
uv run pytest -v

# Node.js projects
npm test
npm run test:coverage

# Commit conventions
git commit -m "test: add failing tests for feature X"
git commit -m "feat: implement feature X to pass tests"
```

### Test Structure Conventions
- Arrange-Act-Assert pattern for test organization
- Clear test isolation with proper setup/teardown
- Mock external dependencies consistently
- Use descriptive assertion messages

## Success Criteria
- ✅ Tests written before implementation
- ✅ Comprehensive test coverage
- ✅ Clear test failure messages
- ✅ Fast test execution

## Common Pitfalls
- ❌ Writing tests after code
- ❌ Testing implementation details instead of behavior
- ❌ Over-complicated test setup
- ❌ Skipping edge cases

## Integration with Other Workflows
- May transition from Discovery-First once requirements clear
- Often combined with Visual Feedback for UI components
- Integrates with CI/CD workflows for automated validation

## TDD Cycle Timing
- Red: 2-5 min | Green: 5-15 min | Refactor: 5-10 min
- Total cycle: Keep under 20 minutes
