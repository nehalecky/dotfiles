# Git Commit Standards

## Commit Message Format

**MANDATORY:** All commits must follow conventional commits specification.

```
<type>(<scope>): <description>

[optional body]
```

### Commit Types
- **feat:** New feature implementation
- **fix:** Bug fixes and corrections  
- **docs:** Documentation updates only
- **style:** Code formatting changes
- **refactor:** Code changes that neither fix bugs nor add features
- **chore:** Maintenance tasks, dependency updates

### Message Principles
- **Explain "why" not just "what"** - Focus on motivation and context
- **Use imperative mood** - "Add feature" not "Added feature"
- **Keep subject line under 50 characters**
- **Reference issues when applicable** - Use "Fixes #123" or "Refs #456"

### Example
```bash
feat: add user authentication with JWT tokens

- Implement login/logout endpoints
- Add JWT middleware for protected routes
- Include refresh token mechanism

Fixes #142
```

## Commit Signing

**MANDATORY:** All commits must be signed using SSH keys.
- Git is configured to automatically sign commits
- Uses 1Password SSH agent for key management
- No additional flags needed - `git commit` triggers signing automatically

## Basic Workflow

```bash
# Stage specific changes
git add path/to/file

# Review staged changes  
git diff --staged

# Commit with conventional message
git commit -m "feat: implement specific functionality"
```