# Essential Tools & Workflows

## Core Workflow: Dotfile Management (chezmoi)

**CRITICAL:** Always follow HOME→Source workflow for dotfile management.

### Workflow Decision Tree
**MANDATORY PRE-ACTION CHECK:**
1. **FILE LOCATION CHECK:**
   - About to edit in `~/.local/share/chezmoi/`? → **STOP! WRONG WORKFLOW**
   - Editing in HOME directory first? → **CONTINUE**

2. **WORKFLOW VERIFICATION:**
   - New file: Create in HOME → Test → `chezmoi add` → Commit
   - Existing file: Edit in HOME → Test → `chezmoi add` → Commit

### PRIMARY WORKFLOW (HOME → Source)
```bash
# Edit actual file in HOME directory
vim ~/.zshrc

# Test the changes work correctly  
source ~/.zshrc

# Sync changes to chezmoi source
chezmoi add ~/.zshrc

# Commit with descriptive message
chezmoi git -- commit -m "feat: add shell configuration"
```

### Essential Conventions
- Always use `$HOME` not `/Users/username` in paths
- Use `chezmoi diff` to preview changes before apply
- Test functionality after each change

## Preferred Tool Suite

| Traditional | Modern Alternative | Key Benefit |
|-------------|-------------------|-------------|
| `grep` | `rg` (ripgrep) | Faster, respects .gitignore |
| `ls` | `eza` | Git integration, tree view |
| `cat` | `bat` | Syntax highlighting |
| `find` | `fd` | Simpler syntax, faster |
| `diff` | `delta` | Enhanced git diffs |

## Essential Command Patterns

### Search and Navigation
```bash
# Search file contents
rg "pattern" --type=js          # Language-specific search
rg "TODO" --context=3           # Show context lines

# Directory listings  
eza -la --tree                  # Tree view with details
eza --git                       # Show git status

# File finding
fd "pattern"                    # Simple file search
fd -e js -e ts                  # Find by extension
```

### File Operations
```bash
# View files with syntax highlighting
bat filename.py

# Preview changes
chezmoi diff                    # Review dotfile changes
delta file1 file2              # Enhanced diff view
```