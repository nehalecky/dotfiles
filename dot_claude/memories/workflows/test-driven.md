# Test-Driven Development Workflow

## Purpose and Scope
For adding new functionality with clear requirements where the interface and expected behavior are well-understood.

## 🔗 Superpowers Skill Integration

**For strict RED-GREEN-REFACTOR TDD execution, use the Superpowers TDD skill:**
```
${SUPERPOWERS_SKILLS_ROOT}/skills/testing/test-driven-development/SKILL.md
```

The Superpowers skill provides:
- Rigid RED-GREEN-REFACTOR discipline
- TodoWrite checklist enforcement
- Bulletproof TDD process tested with subagents
- Step-by-step execution guidance

**This memory provides**: High-level TDD patterns and when to use TDD.
**Superpowers skill provides**: Strict execution discipline and detailed process.

## When to Use
- Adding new functionality with clear requirements
- API development with defined contracts
- Critical business logic requiring high confidence
- Well-understood features where test cases are obvious
- Library or utility function development
- Bug fixes where the desired behavior is clear

## Process Flow

### 1. Write Tests Phase
- **Write failing tests first** that describe the desired behavior
- **Focus on interfaces** and expected outcomes, not implementation details
- **Cover edge cases** and error conditions from the start
- **Use descriptive test names** that explain the expected behavior

### 2. Commit Tests Phase
- **Commit the failing tests** with clear commit message
- **Include test data** and fixtures needed for validation
- **Document test strategy** in commit description
- **Verify tests actually fail** for the right reasons

### 3. Code Phase
- **Implement minimal code** to make tests pass
- **Focus on making tests green** before optimizing
- **Resist over-engineering** during initial implementation
- **Keep implementation simple** and direct

### 4. Iterate Phase
- **Refactor and improve** once tests are passing
- **Add performance optimizations** if needed
- **Enhance error handling** based on test coverage
- **Clean up code structure** while maintaining test coverage

### 5. Commit Implementation Phase
- **Commit working implementation** with descriptive message
- **Reference test coverage** in commit description
- **Include performance notes** if relevant
- **Document any architectural decisions**

## Tool Integration Patterns

### Testing Framework Setup
```bash
# Python projects
uv add pytest pytest-cov        # Test framework with coverage
uv run pytest -v                # Run tests with verbose output

# Node.js projects  
npm test                         # Run configured test suite
npm run test:coverage           # Run with coverage report

# Language-agnostic
git commit -m "test: add failing tests for feature X"
git commit -m "feat: implement feature X to pass tests"
```

### Test Structure Conventions
- Arrange-Act-Assert pattern for test organization
- Clear test isolation with proper setup/teardown
- Mock external dependencies consistently
- Use descriptive assertion messages

## Success Criteria
- ✅ **Comprehensive test coverage** for new functionality
- ✅ **Tests written before implementation** (proof via git history)
- ✅ **Clear test failure messages** when things break
- ✅ **Fast test execution** enabling rapid feedback
- ✅ **Working implementation** that passes all tests

## Common Pitfalls to Avoid
- ❌ **Writing tests after code** defeats the purpose of TDD
- ❌ **Testing implementation details** instead of behavior
- ❌ **Over-complicated test setup** that obscures intent
- ❌ **Ignoring test failures** or making tests pass incorrectly
- ❌ **Skipping edge cases** in initial test design

## Integration with Other Workflows
- May transition **from Discovery-First** once requirements are clear
- Often combined with **Visual Feedback** for UI components with testable logic
- Always incorporates standard **Git Conventions** for test and implementation commits
- Integrates with **CI/CD workflows** for automated validation

## TDD Cycle Timing
- **Red phase:** 2-5 minutes writing failing test
- **Green phase:** 5-15 minutes making test pass  
- **Refactor phase:** 5-10 minutes cleaning up code
- **Total cycle:** Keep under 20 minutes for rapid feedback