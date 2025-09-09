# GitHub MCP Integration

## Overview
GitHub MCP server provides comprehensive integration with GitHub repositories, issues, pull requests, and other GitHub services through the Model Context Protocol.

## Installation

### Standard Installation
```bash
# Install GitHub MCP server
claude mcp add github github.com/github/github-mcp-server

# Verify installation
claude mcp list
# Should show: github: ✓ Connected (github.com/github/github-mcp-server)
```

### Authentication Setup
GitHub MCP requires proper authentication for accessing private repositories and performing write operations:

```bash
# Using GitHub Personal Access Token via 1Password
claude mcp add github github.com/github/github-mcp-server \
  -H "Authorization:Bearer $(op read 'op://Private/github-token/credential')"

# Alternative: Using GitHub CLI authentication
gh auth login
claude mcp add github github.com/github/github-mcp-server
```

### Token Permissions
Required GitHub token scopes for full functionality:
- **`repo`** - Full repository access (private and public)
- **`issues`** - Issue access and management
- **`pull_requests`** - Pull request operations
- **`actions`** - GitHub Actions workflow access
- **`packages`** - Package registry access (if needed)

## Core Functionality

### Repository Operations
```bash
# List repositories
mcp__github__search_repositories "query:user:username"
mcp__github__list_repositories

# Get repository information
mcp__github__get_repository owner repo

# Create new repository
mcp__github__create_repository --name "project-name" --private

# Fork repository
mcp__github__fork_repository owner repo
```

### Issue Management
```bash
# List issues
mcp__github__list_issues owner repo
mcp__github__search_issues "is:open assignee:username"

# Get specific issue
mcp__github__get_issue owner repo issue_number

# Create new issue
mcp__github__create_issue owner repo \
  --title "Issue title" \
  --body "Issue description" \
  --labels "bug,priority:high"

# Update existing issue
mcp__github__update_issue owner repo issue_number \
  --state "closed" \
  --assignees "username"

# Add comment to issue
mcp__github__add_issue_comment owner repo issue_number "Comment text"
```

### Pull Request Workflow
```bash
# List pull requests
mcp__github__list_pull_requests owner repo --state "open"

# Get specific pull request
mcp__github__get_pull_request owner repo pr_number

# Create pull request
mcp__github__create_pull_request owner repo \
  --title "Feature: Add new functionality" \
  --head "feature-branch" \
  --base "main" \
  --body "Description of changes"

# Review pull request
mcp__github__create_pull_request_review owner repo pr_number \
  --event "APPROVE" \
  --body "LGTM! Great work."

# Merge pull request
mcp__github__merge_pull_request owner repo pr_number \
  --merge_method "squash" \
  --commit_title "feat: add new feature"
```

### Branch and Git Operations
```bash
# List branches
mcp__github__list_branches owner repo

# Create branch
mcp__github__create_branch owner repo \
  --branch "feature/new-feature" \
  --from_branch "main"

# Get commit information
mcp__github__get_commit owner repo sha

# List commits
mcp__github__list_commits owner repo --author "username"
```

## Advanced Features

### GitHub Actions Integration
```bash
# List workflows
mcp__github__list_workflows owner repo

# Get workflow runs
mcp__github__list_workflow_runs owner repo workflow_id

# Trigger workflow
mcp__github__run_workflow owner repo workflow_id \
  --ref "main" \
  --inputs '{"environment": "production"}'

# Get workflow job logs
mcp__github__get_job_logs owner repo job_id
```

### Code Search and Analysis
```bash
# Search code across repositories
mcp__github__search_code "function authentication language:python"

# Search within specific repository
mcp__github__search_code "TODO repo:owner/repo"

# Search for security patterns
mcp__github__search_code "password OR secret OR api_key language:javascript"
```

### Release Management
```bash
# List releases
mcp__github__list_releases owner repo

# Get latest release
mcp__github__get_latest_release owner repo

# Create release
mcp__github__create_release owner repo \
  --tag_name "v1.0.0" \
  --name "Version 1.0.0" \
  --body "Release notes" \
  --draft false
```

## Development Workflow Integration

### Issue-Driven Development
```bash
# Daily workflow start
# 1. Check assigned issues
mcp__github__search_issues "is:open assignee:@me"

# 2. Create branch for issue
mcp__github__create_branch owner repo \
  --branch "fix/issue-123-bug-description" \
  --from_branch "main"

# 3. Link commits to issue in commit messages
git commit -m "fix: resolve login timeout issue

Fixes #123"

# 4. Create pull request when ready
mcp__github__create_pull_request owner repo \
  --title "Fix: Resolve login timeout issue (#123)" \
  --head "fix/issue-123-bug-description" \
  --base "main" \
  --body "Resolves #123

## Changes
- Fixed timeout handling in authentication service
- Added retry logic for network requests
- Updated error messages for better UX

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] Manual testing completed"
```

### Code Review Process
```bash
# Review workflow
# 1. Get pull request details
mcp__github__get_pull_request owner repo pr_number

# 2. Get changed files
mcp__github__get_pull_request_files owner repo pr_number

# 3. Add review comments
mcp__github__add_comment_to_pending_review owner repo pr_number \
  --path "src/auth.py" \
  --line 42 \
  --body "Consider adding error handling here"

# 4. Submit review
mcp__github__submit_pending_pull_request_review owner repo pr_number \
  --event "REQUEST_CHANGES" \
  --body "Please address the comments before merging"
```

### Release Automation
```bash
# Release workflow
# 1. Create release branch
mcp__github__create_branch owner repo \
  --branch "release/v1.2.0" \
  --from_branch "develop"

# 2. Update version and changelog
# (manual process or automated via scripts)

# 3. Create pull request for release
mcp__github__create_pull_request owner repo \
  --title "Release v1.2.0" \
  --head "release/v1.2.0" \
  --base "main"

# 4. After merge, create GitHub release
mcp__github__create_release owner repo \
  --tag_name "v1.2.0" \
  --name "Version 1.2.0" \
  --body "$(cat CHANGELOG.md)"
```

## Project Management Integration

### Task and Issue Tracking
```bash
# Weekly planning
# 1. Review current sprint issues
mcp__github__search_issues "is:open milestone:\"Sprint 12\""

# 2. Check blocked issues
mcp__github__search_issues "is:open label:blocked"

# 3. Review pull requests requiring attention  
mcp__github__search_pull_requests "is:open review-requested:@me"

# 4. Check CI/CD status
mcp__github__list_workflow_runs owner repo workflow_id \
  --status "failure"
```

### Team Collaboration
```bash
# Team status checking
# 1. Review team member contributions
mcp__github__list_commits owner repo --author "teammate"

# 2. Check assignment distribution
mcp__github__search_issues "is:open assignee:teammate1"
mcp__github__search_issues "is:open assignee:teammate2"

# 3. Monitor pull request review load
mcp__github__search_pull_requests "is:open review-requested:teammate"
```

## Automation Patterns

### Notification Monitoring
```bash
# Check notifications requiring action
mcp__github__list_notifications

# Filter specific notification types
mcp__github__list_notifications --filter "review_requested"

# Mark notifications as read
mcp__github__mark_all_notifications_read
```

### Repository Health Monitoring
```bash
# Check repository metrics
mcp__github__get_repository owner repo
# Review: stars, forks, open issues, language stats

# Security monitoring
mcp__github__list_dependabot_alerts owner repo
mcp__github__list_secret_scanning_alerts owner repo

# Workflow status monitoring
mcp__github__list_workflow_runs owner repo workflow_id --status "failure"
```

## Integration with Other Tools

### Combine with Jira (via MCP)
```bash
# Cross-reference GitHub issues with Jira tickets
# 1. Get GitHub issue details
github_issue=$(mcp__github__get_issue owner repo issue_number)

# 2. Create or update Jira ticket
mcp__atlassian-mcp__createJiraIssue \
  --summary "GitHub Issue #123: $github_issue_title" \
  --description "Linked to GitHub: https://github.com/owner/repo/issues/123"
```

### Combine with 1Password for Security
```bash
# Secure token rotation
# 1. Generate new GitHub token
# 2. Store in 1Password
op item edit "github-token" credential="new_token_value"

# 3. Update MCP configuration
claude mcp remove github
claude mcp add github github.com/github/github-mcp-server \
  -H "Authorization:Bearer $(op read 'op://Private/github-token/credential')"
```

## Troubleshooting

### Common Issues
```bash
# Rate limit exceeded
# Check current rate limit status
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# Authentication issues
# Verify token permissions and expiration
gh auth status

# Connection problems
# Test with debug logging
CLAUDE_LOG=debug claude mcp test github
```

### Performance Optimization
- **Batch API calls** when possible to avoid rate limits
- **Use specific queries** instead of broad searches
- **Cache results** for repeated operations
- **Monitor API usage** to stay within limits

This module provides comprehensive GitHub integration patterns for efficient development workflow management through MCP.