# 🚀 Ultra-Modern Terminal Tools - Complete Usage Guide

*Transform your development workflow from fragmented GUI apps to a unified terminal powerhouse*

## 🎯 Learning Path: Start Here

### Phase 1: Core Navigation (Week 1)
Learn these first - they replace your most common GUI apps:

1. **📁 File Management** - `Ctrl+a f` (yazi)
2. **✏️ Basic Editing** - `Ctrl+a e` (helix) 
3. **🔄 Git Operations** - `Ctrl+a g` (lazygit)

### Phase 2: Development Workflow (Week 2-3)
4. **🐳 Container Management** - `Ctrl+a d` (lazydocker)
5. **🎮 Workspace Setup** - `Ctrl+a w` (4-pane layout)
6. **📊 System Monitoring** - `Ctrl+a p` (procs)

### Phase 3: Advanced Tools (Week 4+)
7. **☸️ Kubernetes** - `Ctrl+a k` (k9s)
8. **🌐 API Testing** - `Ctrl+a a` (atac)
9. **🔧 Network/Disk Tools** - `Ctrl+a n/u` (bandwhich/dust)

---

## 📁 1. File Management with yazi (`Ctrl+a f`)

**Replaces**: Finder, file explorers, and basic file operations

### Essential Keys
```bash
# Navigation
j/k       # Move up/down
h/l       # Go back/forward in directories
gg/G      # Go to top/bottom
/         # Search files
n/N       # Next/previous search result

# File Operations  
<Space>   # Select file
a         # Select all
d         # Cut selected files
y         # Copy selected files
p         # Paste files
D         # Delete permanently
r         # Rename file

# Views & Modes
Tab       # Toggle preview
t         # Toggle selection mode
.         # Toggle hidden files (period key)
s         # Sort options menu
```

### Power Features
- **Smart Previews**: Markdown files rendered with glow, code with syntax highlighting
- **Image Previews**: Thumbnails for images, PDFs, videos
- **Quick Selection**: `Space` to select multiple files
- **Bulk Operations**: Select files then `d/y/p` for bulk cut/copy/paste
- **Smart Search**: `/` then type filename
- **Hidden Files**: `.` (period) to toggle visibility (not `z` which opens fzf)

### Common Workflows
```bash
# Find and open a project
Ctrl+a f → / → "project-name" → Enter → hx main.py

# Bulk file organization
Ctrl+a f → Tab (select files) → Space Space Space → d → navigate → p

# Quick file preview
Ctrl+a f → navigate to file → Tab (preview opens)
```

---

## ✏️ 2. Code Editing with Helix (`Ctrl+a e`)

**Replaces**: VS Code for quick edits, Vim/Nano for terminal editing

### Modal Editing Basics
Helix uses vim-like modes but with built-in selections:

```bash
# Modes
<Esc>     # Normal mode (default)
i         # Insert mode
v         # Visual mode (select)
:         # Command mode

# Essential Movement (Normal Mode)
h/j/k/l   # Left/down/up/right
w/b       # Word forward/backward
0/$       # Start/end of line
gg/G      # Start/end of file

# Selection & Editing
v         # Start selection
d         # Delete selection
y         # Copy (yank) selection
p         # Paste after cursor
u         # Undo
Ctrl+r    # Redo
```

### Built-in LSP Features (No setup needed!)
```bash
gd        # Go to definition
gr        # Go to references
K         # Show hover info
<Space>a  # Code actions
<Space>s  # Symbol search
<Space>f  # File picker
<Space>/  # Global search
```

### Common Workflows
```bash
# Quick file edit
Ctrl+a e → <Space>f → type filename → Enter → edit → :w → :q

# Multi-file project work
Ctrl+a e → <Space>f (file picker) → work on files → <Space>s (symbol search)

# Search and replace across project
Ctrl+a e → <Space>/ → type search → Enter → edit each occurrence
```

### Learning Tips
- **Start Simple**: Use `i` to insert, `Esc` to exit, `:w` to save, `:q` to quit
- **Use Built-ins**: File picker (`<Space>f`) is faster than manual navigation
- **LSP is Magic**: `gd` (go to definition) works out of the box for most languages

---

## 🔄 3. Git Management with lazygit (`Ctrl+a g`)

**Replaces**: GitHub Desktop, SourceTree, git command line

### Main Interface Layout
```
Status     Branches    Files       Commits
  |          |          |           |
[Working]  [main]    [modified]  [history]
[Staged]   [dev]     [untracked] [details]
```

### Essential Keys
```bash
# Navigation
Tab/Shift+Tab  # Switch between panels
j/k            # Move up/down in current panel
h/l            # Move left/right between panels

# File Operations (Files panel)
<Space>        # Stage/unstage file
a              # Stage all files
d              # View diff
e              # Edit file
D              # Discard changes

# Commit Operations (Status panel)
c              # Commit staged changes
A              # Amend last commit
P              # Push to remote
p              # Pull from remote

# Branch Operations (Branches panel)
<Space>        # Checkout branch
n              # New branch
d              # Delete branch
r              # Rebase
m              # Merge
```

### Common Workflows

**Daily Commit Workflow:**
```bash
Ctrl+a g
→ Tab to Files panel
→ Space Space Space (stage files)
→ Tab to Status panel  
→ c (commit) → type message → Enter
→ P (push)
```

**Branch Management:**
```bash
Ctrl+a g
→ Tab to Branches panel
→ n (new branch) → type name → Enter
→ work on code...
→ return to lazygit → stage → commit → P (push)
```

**Conflict Resolution:**
```bash
Ctrl+a g → pull conflicts appear
→ Tab to Files panel → Enter on conflicted file
→ resolve in editor → save
→ return to lazygit → Space (stage resolved)
→ c (commit merge)
```

---

## 🐳 4. Container Management with lazydocker (`Ctrl+a d`)

**Replaces**: Docker Desktop, container GUIs

### Interface Panels
```
Containers    Images      Volumes     Services
    |           |           |           |
[running]   [alpine]    [data]    [web-stack]
[stopped]   [node]      [logs]    [database]
```

### Essential Keys
```bash
# Navigation
Tab           # Switch panels
j/k           # Move up/down
Enter         # View details/logs

# Container Operations
r             # Restart container
s             # Stop container
d             # Delete container
l             # View logs
e             # Exec into container (shell)

# System Operations
p             # Prune unused containers/images
Space         # Start/stop container
```

### Common Workflows

**Development Container Management:**
```bash
Ctrl+a d
→ see running containers
→ Enter on container → view logs
→ e (exec) → get shell access
```

**Cleanup & Maintenance:**
```bash
Ctrl+a d
→ Tab to Images panel
→ d d d (delete unused images)
→ p (prune system)
```

**Debug Container Issues:**
```bash
Ctrl+a d
→ find problematic container
→ l (view logs) → diagnose issue
→ r (restart) or e (exec for debugging)
```

---

## 🎮 5. Development Workspace (`Ctrl+a w`)

**The Magic**: Instantly creates a 4-pane development environment

### Auto-Layout
```
┌─────────────┬─────────────┐
│             │             │
│   MAIN      │   PROCS     │
│ (terminal)  │ (processes) │  
│             │             │
├─────────────┼─────────────┤
│             │             │
│  LAZYGIT    │   EXTRA     │
│   (git)     │ (scratch)   │
│             │             │
└─────────────┴─────────────┘
```

### Navigation Between Panes
```bash
Ctrl+a h/j/k/l    # Move between panes (vim-style)
Ctrl+a |          # Split right manually  
Ctrl+a -          # Split down manually
Ctrl+a x          # Close current pane
Ctrl+a z          # Toggle pane zoom
```

### Workspace Workflow
```bash
# Start development session
Ctrl+a w
→ Main pane: cd to project, start dev server
→ Git pane: already running lazygit for commits
→ Process pane: procs showing running processes
→ Extra pane: run tests, logs, or additional terminal
```

### Pro Tips
- **Main pane**: Your primary work area (coding, running commands)
- **Git pane**: Quick commits without leaving your workflow
- **Process pane**: Lightweight process monitoring (sort with c/m/p)
- **Extra pane**: Perfect for running tests, tailing logs, or quick commands

---

## 📊 6. System Monitoring with procs (`Ctrl+a p`)

**Replaces**: Activity Monitor, htop, ps command

### Interface & Controls
```bash
# Sorting
c             # Sort by CPU
m             # Sort by memory  
p             # Sort by PID
n             # Sort by name

# Filtering
/             # Search processes
q             # Quit
r             # Refresh rate
k             # Kill process (be careful!)
```

### What to Monitor
- **High CPU**: Look for runaway processes
- **Memory Usage**: Find memory leaks
- **Development Tools**: Monitor your dev servers, databases
- **Background Apps**: Identify resource hogs

### Common Workflows
```bash
# Find resource-heavy processes
Ctrl+a p → c (sort by CPU) → identify problems

# Monitor development environment
Ctrl+a p → / → "node" → Enter (find all Node processes)

# System cleanup
Ctrl+a p → identify unused apps → k (kill if needed)
```

---

## ☸️ 7. Kubernetes with k9s (`Ctrl+a k`)

**Replaces**: Kubernetes Dashboard, kubectl commands

### Essential Navigation
```bash
# Resource Types
:pods         # View pods
:services     # View services  
:deployments  # View deployments
:nodes        # View nodes
:events       # View cluster events

# Pod Operations
d             # Delete resource
l             # View logs
s             # Shell into pod
Enter         # View resource details
```

### Common Workflows

**Pod Debugging:**
```bash
Ctrl+a k
→ :pods → find problematic pod
→ l (logs) → diagnose issue
→ s (shell) → debug inside container
```

**Service Discovery:**
```bash
Ctrl+a k
→ :services → find your service
→ Enter → view endpoints and details
```

### Learning Progression
1. **Start with**: `:pods` - see what's running
2. **Then explore**: `:services`, `:deployments`
3. **Advanced usage**: `:events` for cluster issues

---

## 🌐 8. API Testing with atac (`Ctrl+a a`)

**Replaces**: Postman, Insomnia, curl commands

### Interface Basics
```bash
# Navigation
Tab           # Switch between panels (URLs, Headers, Body, Response)
j/k           # Move up/down
Enter         # Execute request

# Request Building
n             # New request
e             # Edit current field
d             # Delete request
```

### Common Workflows

**Quick API Test:**
```bash
Ctrl+a a
→ n (new request)
→ type URL → Tab to method → change to POST
→ Tab to body → add JSON payload
→ Enter (send request)
```

**API Development Workflow:**
```bash
# Build and test API endpoints
Ctrl+a a → build request → test
→ switch to editor → fix code
→ back to atac → retest
```

---

## 🔧 9. Network & Disk Tools

### Network Monitoring - bandwhich (`Ctrl+a n`)
```bash
# Shows network usage by process
Ctrl+a n → see which apps are using bandwidth
→ helpful for identifying network-heavy processes
→ q to quit
```

### Disk Usage - dust (`Ctrl+a u`)
```bash
# Modern du replacement
Ctrl+a u → see directory sizes in current location
→ helps identify large files/directories for cleanup
→ automatically exits when done
```

---

## 🎯 Putting It All Together: Real Workflows

### Morning Development Routine
```bash
1. Ctrl+a w                    # Launch 4-pane workspace
2. Main pane: cd project && npm run dev
3. Git pane: already has lazygit open
4. Process pane: watching running processes
5. Extra pane: npm test --watch
```

### Bug Investigation
```bash
1. Ctrl+a g                    # Check recent commits
2. Ctrl+a d                    # Check if containers are healthy
3. Ctrl+a p                    # Look for resource issues
4. Ctrl+a a                    # Test API endpoints
5. Ctrl+a e                    # Edit code to fix
```

### Project Cleanup
```bash
1. Ctrl+a f                    # Navigate to project
2. Ctrl+a u                    # Check disk usage
3. Ctrl+a d                    # Clean up containers
4. Ctrl+a g                    # Clean up git branches
```

---

## 🏆 Pro Tips for Mastery

### 1. Muscle Memory Development
- **Week 1**: Focus on `Ctrl+a f/e/g` only
- **Week 2**: Add `Ctrl+a w/d` for development workflow
- **Week 3**: Start using monitoring tools `Ctrl+a p/n/u`
- **Week 4+**: Master advanced tools `Ctrl+a k/a`

### 2. Integration Patterns
- **Always start with workspace**: `Ctrl+a w` for any serious development
- **File → Edit cycle**: `Ctrl+a f` → find file → `Ctrl+a e` → edit
- **Code → Git cycle**: Write code → `Ctrl+a g` → stage → commit
- **Debug cycle**: `Ctrl+a p/d` → identify issue → `Ctrl+a e` → fix

### 3. Escape Hatches
- **Overwhelmed?** Start with just file manager (`Ctrl+a f`)
- **Tools not working?** Use `wezterm-shortcuts` to see what's available
- **Need GUI?** All tools coexist with traditional apps
- **Stuck in a tool?** `q` or `Ctrl+c` usually exits

### 4. Learning Resources
- **Built-in help**: Most tools have `?` or `h` for help
- **Man pages**: `man hx`, `man lazygit` etc.
- **Practice projects**: Use these tools on small projects first

---

## 🚀 Getting Started Action Plan

### This Week 
1. **Just use the file manager**: `Ctrl+a f` for all file navigation
2. **Try basic editing**: `Ctrl+a e` → `i` (insert) → type → `Esc` → `:w` → `:q`
3. **Git with confidence**: `Ctrl+a g` → stage files with `Space` → `c` to commit

### Next Week
4. **Launch workspaces**: `Ctrl+a w` for development sessions
5. **Monitor your system**: `Ctrl+a p` to see what's running
6. **Manage containers**: `Ctrl+a d` if you use Docker

### Remember
- **Start small** - don't try to learn everything at once
- **Use what works** - traditional tools still exist if you need them  
- **Practice daily** - muscle memory takes time to develop
- **Have fun** - this setup makes development genuinely more enjoyable!

The tools are designed to work together seamlessly. Once you build the muscle memory for the leader key system, you'll wonder how you ever developed without it! 🎯

---

## 📖 Quick Reference

### Leader Key Shortcuts
```bash
Ctrl+a f    # 📁 File manager (yazi)
Ctrl+a e    # ✏️  Editor (helix)  
Ctrl+a g    # 🔄 Git (lazygit)
Ctrl+a d    # 🐳 Docker (lazydocker)
Ctrl+a k    # ☸️  Kubernetes (k9s)
Ctrl+a a    # 🌐 API client (atac)
Ctrl+a p    # 📊 Process monitor (procs)
Ctrl+a n    # 🌐 Network monitor (bandwhich)
Ctrl+a u    # 💾 Disk usage (dust)
Ctrl+a s    # 🔧 Session manager (zellij)
Ctrl+a w    # 🎮 Launch 4-pane workspace
```

### Universal Exit Commands
```bash
q           # Quit most TUI applications
Ctrl+c      # Force quit (universal)
:q          # Vim-style quit (helix, etc.)
Ctrl+a x    # Close WezTerm pane
```

*Experience the future of terminal-first development!*