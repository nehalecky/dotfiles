# Public Repository Posting Protocol

## CRITICAL SAFETY REQUIREMENT

**MANDATORY USER APPROVAL FOR PUBLIC REPOSITORY OPERATIONS**

This protocol applies to ALL agents performing operations that post content to public repositories (GitHub, GitLab, Bitbucket, or any other platform).

## Core Principle

Before ANY operation that posts content to public repositories, you MUST obtain explicit user approval.

## Required Steps

### 1. Present Complete Content
Show the user exactly what will be posted, including:
- Full text of issues, comments, PR descriptions, or file content
- Target repository name and visibility status (public/private)
- Any labels, assignees, metadata, or configuration changes
- Platform (GitHub, GitLab, Bitbucket, etc.)

### 2. Request Explicit Approval

Use this exact format:

```
I am ready to post the following to the PUBLIC repository [owner/repository]:

Platform: [GitHub/GitLab/Bitbucket/Other]

===== CONTENT PREVIEW =====
[FULL CONTENT EXACTLY AS IT WILL APPEAR]
===========================

This will be publicly visible to all users on [platform].

Do you approve this public posting? Please confirm YES to proceed.
```

### 3. Wait for Confirmation

**NEVER proceed without explicit user approval.**

Valid approval responses:
- "YES"
- "Yes, proceed"
- "Approved"
- "Go ahead"

NOT valid without explicit confirmation:
- Silence
- Continued conversation on another topic
- Implied consent

### 4. Operations Requiring Approval

The following operations REQUIRE approval when performed on PUBLIC repositories:

#### Repository Operations
- Creating issues
- Creating pull/merge requests
- Adding comments to issues/PRs/MRs
- Creating or updating files
- Creating or updating wikis
- Any operation creating publicly visible content

#### Organization Operations
- Posting to organization discussions
- Creating organization-wide issues
- Publishing organization documentation

## Exceptions

### Read-Only Operations (No Approval Required)
- Searching repositories
- Viewing issues, PRs, or files
- Listing repositories or branches
- Getting repository metadata
- Searching code
- Reading notifications

### Local Operations (No Approval Required)
- Local git commits
- Local branch creation
- Local file modifications
- Local repository initialization

### Private Repository Operations
- May proceed without approval for private repositories
- MUST inform user of the operation being performed
- Still maintain good practices for documentation and clarity

## Verification Before Posting

Before requesting approval, verify:
- [ ] Repository visibility is correctly identified (public vs private)
- [ ] Content preview is complete and accurate
- [ ] Target repository and branch are correct
- [ ] No sensitive information (credentials, tokens, personal data) in content
- [ ] Operation is appropriate for the repository's purpose

## Error Handling

If uncertain about repository visibility:
1. Check repository metadata first
2. Default to treating as PUBLIC (safer)
3. Request approval following full protocol

## Emergency Override

In rare cases of urgent bug fixes or security issues:
1. Clearly mark the urgency in the approval request
2. Still show full content for transparency
3. Explain why immediate action is needed
4. Proceed only after explicit emergency approval

## Integration with Agents

All agents performing repository operations must:
- Import and follow this protocol
- Never rationalize bypassing approval
- Treat user safety as paramount
- Document when approval was obtained

## Platform-Specific Notes

### GitHub
- Public repositories are clearly marked
- Organization repositories may be public
- Forked repositories inherit original visibility

### GitLab
- Projects can be public, internal, or private
- Groups can have different visibility settings
- Subgroups inherit parent visibility by default

### Bitbucket
- Workspaces can be public or private
- Repository visibility is independent of workspace

## Remember

**When in doubt, ask for approval. User safety and consent are non-negotiable.**

Unauthorized public posting violates user trust and can have serious professional, legal, or security consequences.
