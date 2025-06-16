# Claude Code Emacs Integration Guide

A comprehensive guide for using claude-code.el with Doom Emacs to enhance your development workflow with AI assistance.

## Table of Contents
- [Overview](#overview)
- [Installation Status](#installation-status)
- [Basic Commands](#basic-commands)
- [Practical Workflows](#practical-workflows)
- [Real-World Examples](#real-world-examples)
- [Doom Emacs Integration](#doom-emacs-integration)
- [Pro Tips](#pro-tips)

## Overview

claude-code.el provides seamless integration between Claude Code CLI and Emacs, allowing you to:
- Get AI assistance without leaving your editor
- Maintain context across coding sessions
- Send code snippets with full file context
- Access Claude's slash commands via transient menus
- Run multiple Claude instances for different projects

## Installation Status

✅ **Already Installed and Configured!**
- Package declaration in `~/.config/doom/packages.el`
- Configuration in `~/.config/doom/config.el`
- Keybinding prefix: `C-c c`

## Basic Commands

All commands are prefixed with `C-c c` (customizable):

| Command | Keybinding | Description |
|---------|------------|-------------|
| Start Claude | `C-c c c` | Start a new Claude session |
| | `C-u C-c c c` | Start and switch to Claude buffer |
| | `C-u C-u C-c c c` | Continue previous conversation |
| | `C-u C-u C-u C-c c c` | Prompt for project directory |
| Toggle Window | `C-c c t` | Show/hide Claude window |
| Send Command | `C-c c s` | Send a command to Claude |
| Send with Context | `C-c c x` | Send command with current file/line info |
| Send Region | `C-c c r` | Send selected text to Claude |
| | `C-u C-c c r` | Send region with custom prompt |
| Fix Error | `C-c c e` | Ask Claude to fix error at point |
| Slash Commands | `C-c c /` | Access Claude's slash command menu |
| All Commands | `C-c c m` | Show transient menu with all commands |
| Switch Buffer | `C-c c b` | Switch to Claude buffer |
| Kill Session | `C-c c k` | Kill current Claude session |
| | `C-u C-c c k` | Kill ALL Claude sessions |

## Practical Workflows

### 1. Code Analysis Workflow
```elisp
;; Understanding unfamiliar code
;; 1. Open a complex file
;; 2. Position cursor on confusing function
;; 3. C-c c x (send with context)
;; 4. Type: "Explain this function and its role in the codebase"
```

### 2. Refactoring Assistant
```elisp
;; Improving code quality
;; 1. Select code region (C-SPC and navigate)
;; 2. C-c c r (send region)
;; 3. Ask: "Refactor this for better readability and performance"
;; 4. Review suggestions and apply
```

### 3. Test Generation
```elisp
;; Creating comprehensive tests
;; 1. Write your function
;; 2. Select the entire function
;; 3. C-c c r
;; 4. "Generate unit tests for this function using [pytest/jest/etc]"
```

### 4. Documentation Helper
```elisp
;; Writing better documentation
;; 1. Select function or class
;; 2. C-u C-c c r (with prompt)
;; 3. "Write comprehensive docstring following [NumPy/Google] style"
```

### 5. Debugging Session
```elisp
;; Interactive debugging
;; 1. Start Claude: C-c c c
;; 2. When error occurs, copy error message
;; 3. C-c c s → Paste error
;; 4. Ask: "Why is this happening and how do I fix it?"
;; 5. Keep Claude open for follow-up questions
```

## Real-World Examples

### Example 1: Learning a New Codebase
```bash
# Start Claude with project context
C-u C-u C-u C-c c c
# Select project root when prompted

# Then ask questions like:
"What's the architecture of this project?"
"Where is authentication handled?"
"How does the data flow through the application?"
```

### Example 2: Code Review Before Commit
```elisp
;; In your file with changes
;; 1. Select all changes (or use git-gutter to see them)
;; 2. C-c c r
;; 3. "Review this code for:
;;    - Potential bugs
;;    - Security issues  
;;    - Performance problems
;;    - Code style violations"
```

### Example 3: API Integration
```elisp
;; When working with a new API
;; 1. C-c c s
;; 2. "Show me how to integrate with [API name] in Python
;;    including error handling and rate limiting"
```

### Example 4: Refactoring Legacy Code
```elisp
;; Select old function
;; C-c c r
;; "Modernize this code using current Python best practices,
;;  add type hints, and improve error handling"
```

## Doom Emacs Integration

### With Magit
```elisp
;; In magit-status buffer
;; 1. Stage your changes
;; 2. Press 'c' for commit
;; 3. C-c c s in commit message buffer
;; 4. "Write a commit message for the staged changes"
```

### With LSP-mode
```elisp
;; When LSP shows errors/warnings
;; 1. Navigate to error with `] d` (next diagnostic)
;; 2. C-c c e (fix error at point)
;; 3. Claude analyzes with full context
```

### With Evil Mode
```elisp
;; Visual mode selections
;; 1. Press 'v' for visual mode
;; 2. Select code with vim motions
;; 3. C-c c r to send selection
```

### With Projectile
```elisp
;; Project-wide assistance
;; 1. C-c p p (switch project)
;; 2. C-u C-u C-u C-c c c
;; 3. Claude now understands your whole project
```

## Pro Tips

### 1. **Multiple Instances**
Run different Claude instances for different concerns:
- One for general coding
- One for debugging
- One for documentation

### 2. **Persistent Context**
Unlike the web interface, your conversation persists. Use this for:
- Long debugging sessions
- Iterative refactoring
- Learning new concepts

### 3. **Fork Conversations**
Use `C-c c f` to branch conversations when:
- Exploring different solutions
- Trying alternative approaches
- Keeping one conversation focused

### 4. **Quick Access Patterns**
```elisp
;; Add to your config.el for even faster access
(map! :leader
      (:prefix ("a" . "ai")
       :desc "Claude send region" "r" #'claude-code-send-region
       :desc "Claude fix error" "e" #'claude-code-fix-error-at-point
       :desc "Claude with context" "x" #'claude-code-send-command-with-context))
```

### 5. **Template Prompts**
Create snippets for common queries:
```elisp
;; Using yasnippet
# -*- mode: snippet -*-
# name: claude-review
# key: creview
# --
Review this code for:
- Logic errors
- Edge cases
- Performance issues
- Security concerns
- Code style (PEP8/ESLint)
$0
```

### 6. **Read-Only Mode**
When Claude returns long responses:
- Switch to read-only mode for easier navigation
- Use Emacs search (`C-s`) to find specific parts
- Copy code snippets without terminal escape sequences

## Common Use Cases

1. **"What does this do?"** - Understanding unfamiliar code
2. **"Fix this error"** - Debugging assistance
3. **"Write tests"** - Test generation
4. **"Improve this"** - Code optimization
5. **"Add types"** - Type annotation help
6. **"Document this"** - Documentation generation
7. **"Is this secure?"** - Security review
8. **"Make this faster"** - Performance optimization

## Troubleshooting

If Claude Code doesn't respond:
1. Check if CLI is running: `pgrep -f claude`
2. Restart session: `C-c c k` then `C-c c c`
3. Verify claude CLI works: Run `claude` in terminal

---

*Remember: Claude Code in Emacs gives you AI assistance without context switching. Use it to stay in flow while coding!*