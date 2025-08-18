# Terminal Guide

*Transform your development workflow with a unified terminal-first environment*

## Quick Start

### Learning Path: Start Here

**Phase 1: Core Navigation (Week 1)**
Learn these first - they replace your most common GUI apps:

1. **File Management** - `Ctrl+a f` (yazi)
2. **Basic Editing** - `Ctrl+a e` (helix) 
3. **Git Operations** - `Ctrl+a g` (lazygit)

**Phase 2: Development Workflow (Week 2-3)**
4. **Container Management** - `Ctrl+a d` (lazydocker)
5. **Workspace Setup** - `Ctrl+a w` (4-pane layout)
6. **System Monitoring** - `Ctrl+a p` (procs)

**Phase 3: Advanced Tools (Week 4+)**
7. **Kubernetes** - `Ctrl+a k` (k9s)
8. **API Testing** - `Ctrl+a a` (atac)
9. **Network/Disk Tools** - `Ctrl+a n/u` (bandwhich/dust)

### Universal Exit Commands
```bash
q           # Quit most TUI applications
Ctrl+c      # Force quit (universal)
:q          # Vim-style quit (helix, etc.)
Ctrl+a x    # Close WezTerm pane
```

## WezTerm Configuration & Setup

### Key Features

**Leader Key System**
- **Leader**: `Ctrl+a` (similar to tmux)
- **Timeout**: 1000ms
- **Visual indicator**: Shows "LEADER" in status bar when active

### Pane Management

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Split Vertical | `Ctrl+a \|` | Split pane vertically |
| Split Horizontal | `Ctrl+a -` | Split pane horizontally |
| Navigate Left | `Ctrl+a h` | Move to pane on the left |
| Navigate Right | `Ctrl+a l` | Move to pane on the right |
| Navigate Up | `Ctrl+a k` | Move to pane above |
| Navigate Down | `Ctrl+a j` | Move to pane below |
| Resize Left | `Ctrl+a Shift+H` | Increase pane size left |
| Resize Right | `Ctrl+a Shift+L` | Increase pane size right |
| Resize Up | `Ctrl+a Shift+K` | Increase pane size up |
| Resize Down | `Ctrl+a Shift+J` | Increase pane size down |
| Close Pane | `Ctrl+a x` | Close current pane (with confirmation) |
| Zoom Toggle | `Ctrl+a z` | Toggle pane zoom state |

### Configuration Details

**Font Settings**
- **Font**: MesloLGS NF (Nerd Font)
- **Size**: 12pt
- **Ligatures**: Enabled (calt, clig, liga)

**Color Scheme**
- Based on Monokai/iTerm2 dark theme
- Custom ANSI colors for optimal visibility
- Hyperlink detection enabled

**Window Behavior**
- **Decorations**: RESIZE (for yabai compatibility)
- **Resize Increments**: Cell-based (terminal grid)
- **Initial Size**: 80x25
- **Padding**: 2px all sides

**Performance**
- **GPU Acceleration**: WebGpu frontend
- **Max FPS**: 120
- **Scrollback**: 1000 lines

### macOS Compatibility Shortcuts

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Delete Word | `Option + Backspace` | Delete word backward |
| Beginning of Line | `Cmd + ←` | Jump to line start |
| End of Line | `Cmd + →` | Jump to line end |
| Word Left | `Option + ←` | Jump word backward |
| Word Right | `Option + →` | Jump word forward |
| Delete to Beginning | `Cmd + Backspace` | Delete to line start |
| Delete Word Forward | `Option + Delete` | Delete word forward |

### Status Bar

The status bar displays:
- **Left**: Current working directory (with `~` for home)
- **Right**: LEADER indicator when leader key is active

## Workspace Management

### Dual Workspace System

**Philosophy**: Separate concerns between daily operations and focused development

### Home Command Center (`workspace-home`)

**Purpose**: Daily operations, dotfiles management, system monitoring

**Layout**: 4-panel environment optimized for daily tasks
```
┌─────────────────┬─────────────────────────────────┐
│ Terminal (zsh)  │ File Manager (yazi)             │
│ Chezmoi source  │ Browse dotfiles                 │
├─────────────────┼─────────────────────────────────┤
│ Claude Code     │ Task Management                 │
│ Auto-launch AI  │ Daily task tracking             │
└─────────────────┴─────────────────────────────────┘
```

**Usage Pattern**:
- **Morning routine**: Check tasks, sync dotfiles
- **Configuration work**: Edit dotfiles, test changes, commit updates
- **System maintenance**: Monitor processes, check disk usage, update packages

### Project Development (`workspace-dev`)

**Purpose**: Focused development on specific projects

**Layout**: 4-panel environment optimized for coding
```
┌─────────────────┬─────────────────────────────────┐
│ Terminal/REPL   │ Editor (Helix)                  │
│ Project context │ Smart language detection        │
├─────────────────┼─────────────────────────────────┤
│ Git (lazygit)   │ Monitor/Tests                   │
│ Version control │ Project-specific tools          │
└─────────────────┴─────────────────────────────────┘
```

**Usage Pattern**:
- **Code development**: Edit in Helix, run commands in terminal
- **Version control**: Stage changes in lazygit, review diffs
- **Testing/Building**: Monitor test output, build processes
- **Debugging**: REPL interaction, log monitoring

### Workspace Commands

**Keyboard Shortcuts**:
```bash
Ctrl+a w                      # Launch 4-tile development workspace (legacy)
Ctrl+a h                      # Launch Home Command Center
Ctrl+a Shift+W               # Launch project workspace  
Ctrl+a r                      # Refresh current workspace
Cmd+Enter                     # Toggle fullscreen
```

**Command Line (Tab-completion friendly)**:
```bash
workspace-home                # Home Command Center (dotfiles/daily ops)
workspace-dev [project]       # Project development environment
workspace-refresh            # Refresh workspace data
```

### Session Management
```bash
# Start predefined sessions
workspace-home                # Daily operations setup
workspace-dev myproject       # Project-specific environment

# Session persistence  
zellij list-sessions          # Show active sessions
zellij attach session-name   # Reconnect to session
zellij kill-session name     # Terminate session
```

## TUI Tools Usage

### File Management with yazi (`Ctrl+a f`)

**Replaces**: Finder, file explorers, and basic file operations

**Essential Keys**:
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

**Power Features**:
- **Smart Previews**: Markdown files rendered with glow, code with syntax highlighting
- **Image Previews**: Thumbnails for images, PDFs, videos
- **Quick Selection**: `Space` to select multiple files
- **Bulk Operations**: Select files then `d/y/p` for bulk cut/copy/paste
- **Smart Search**: `/` then type filename
- **Hidden Files**: `.` (period) to toggle visibility

### Code Editing with Helix (`Ctrl+a e`)

**Replaces**: VS Code for quick edits, Vim/Nano for terminal editing

**Modal Editing Basics**:
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

**Built-in LSP Features** (No setup needed!):
```bash
gd        # Go to definition
gr        # Go to references
K         # Show hover info
<Space>a  # Code actions
<Space>s  # Symbol search
<Space>f  # File picker
<Space>/  # Global search
```

### Git Management with lazygit (`Ctrl+a g`)

**Replaces**: GitHub Desktop, SourceTree, git command line

**Essential Keys**:
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

### Container Management with lazydocker (`Ctrl+a d`)

**Replaces**: Docker Desktop, container GUIs

**Essential Keys**:
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

### System Monitoring with procs (`Ctrl+a p`)

**Replaces**: Activity Monitor, htop, ps command

**Interface & Controls**:
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

### Kubernetes with k9s (`Ctrl+a k`)

**Replaces**: Kubernetes Dashboard, kubectl commands

**Essential Navigation**:
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

### API Testing with atac (`Ctrl+a a`)

**Replaces**: Postman, Insomnia, curl commands

**Interface Basics**:
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

### Network & Disk Tools

**Network Monitoring - bandwhich (`Ctrl+a n`)**:
```bash
Ctrl+a n      # Shows network usage by process
q             # Quit
```

**Disk Usage - dust (`Ctrl+a u`)**:
```bash
Ctrl+a u      # See directory sizes in current location
# Automatically exits when done
```

## Advanced Workflows

### Real Development Workflows

**Morning Development Routine**:
```bash
1. Ctrl+a w                    # Launch 4-pane workspace
2. Main pane: cd project && npm run dev
3. Git pane: already has lazygit open
4. Process pane: watching running processes
5. Extra pane: npm test --watch
```

**Bug Investigation**:
```bash
1. Ctrl+a g                    # Check recent commits
2. Ctrl+a d                    # Check if containers are healthy
3. Ctrl+a p                    # Look for resource issues
4. Ctrl+a a                    # Test API endpoints
5. Ctrl+a e                    # Edit code to fix
```

**Project Cleanup**:
```bash
1. Ctrl+a f                    # Navigate to project
2. Ctrl+a u                    # Check disk usage
3. Ctrl+a d                    # Clean up containers
4. Ctrl+a g                    # Clean up git branches
```

### Integration Patterns

**Development Workflow Integration**:
1. **Start session**: `workspace-dev project-name`
2. **Edit code**: Helix in dedicated panel
3. **Test changes**: Terminal REPL/build commands
4. **Version control**: Lazygit for staging/committing
5. **Monitor**: Watch panel for test results/logs

**Daily Operations Integration**:
1. **Morning setup**: `workspace-home` for daily context
2. **Check tasks**: Task management panel
3. **System work**: Terminal for dotfiles/system management

**Muscle Memory Development**:
- **Week 1**: Focus on `Ctrl+a f/e/g` only
- **Week 2**: Add `Ctrl+a w/d` for development workflow
- **Week 3**: Start using monitoring tools `Ctrl+a p/n/u`
- **Week 4+**: Master advanced tools `Ctrl+a k/a`

### Common Workflow Patterns

**File → Edit cycle**: `Ctrl+a f` → find file → `Ctrl+a e` → edit
**Code → Git cycle**: Write code → `Ctrl+a g` → stage → commit
**Debug cycle**: `Ctrl+a p/d` → identify issue → `Ctrl+a e` → fix

## Troubleshooting

### Performance Optimization

**Startup Time Targets**:
- **Workspace launch**: < 2 seconds for full 4-panel setup
- **TUI application startup**: < 500ms for individual tools
- **Git operations**: < 1 second for status/diff operations

**Memory Management**:
- **Session sharing**: Reuse existing TUI sessions when possible
- **Lazy loading**: Start applications only when panels become active
- **Resource cleanup**: Automatic cleanup of idle sessions

### Common Issues

**Font Not Found**:
If you see font warnings, ensure MesloLGS NF is installed:
```bash
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font
```

**Pane Navigation Not Working**:
Ensure no other applications are intercepting `Ctrl+a`. Check:
- System keyboard shortcuts
- Other terminal multiplexers (tmux/screen)

**Status Bar Not Updating**:
The status bar updates every second. If not visible:
- Check `enable_tab_bar = true`
- Verify `hide_tab_bar_if_only_one_tab = false`

**Tools Not Working**:
- Use `wezterm-shortcuts` to see what's available
- Most tools have `?` or `h` for help
- `q` or `Ctrl+c` usually exits stuck applications

### Escape Hatches

- **Overwhelmed?** Start with just file manager (`Ctrl+a f`)
- **Need GUI?** All tools coexist with traditional apps
- **Learning curve?** Practice on small projects first

### Learning Resources

- **Built-in help**: Most tools have `?` or `h` for help
- **Man pages**: `man hx`, `man lazygit` etc.
- **Practice projects**: Use these tools on small projects first

## Getting Started Action Plan

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

The tools are designed to work together seamlessly. Once you build the muscle memory for the leader key system, you'll wonder how you ever developed without it!