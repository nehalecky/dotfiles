# Tool Reference

Complete catalog of installed tools, commands, and shortcuts for development and system management.

## Table of Contents
- [Core Tools](#core-tools)
- [Command Reference](#command-reference)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Quick Reference](#quick-reference)

## Core Tools

### Package Managers

| Tool | Purpose | Key Commands |
|------|---------|--------------|
| [Homebrew](https://brew.sh/) | macOS package manager | `brew install`, `brew upgrade`, `brew bundle` |
| [uv](https://docs.astral.sh/uv/) | Python package installer | `uv add`, `uv run`, `uv sync` |
| [pnpm](https://pnpm.io/) | Node.js package manager | `pnpm install`, `pnpm add`, `pnpm run` |
| [pdm](https://pdm.fming.dev/) | Python package manager | `pdm add`, `pdm install`, `pdm run` |

### Modern CLI Replacements

| Traditional | Modern Tool | Key Benefit | Installation |
|-------------|-------------|-------------|--------------|
| `cat` | [bat](https://github.com/sharkdp/bat) | Syntax highlighting, Git integration | `brew install bat` |
| `ls` | [eza](https://eza.rocks/) | Colors, icons, Git status | `brew install eza` |
| `grep` | [ripgrep](https://github.com/BurntSushi/ripgrep) | Faster search, smart defaults | `brew install ripgrep` |
| `find` | [fd](https://github.com/sharkdp/fd) | Simpler syntax, faster | `brew install fd` |
| `diff` | [delta](https://github.com/dandavison/delta) | Enhanced git diffs | `brew install git-delta` |
| `top` | [btop](https://github.com/aristocratos/btop) | Mouse support, better UI | `brew install btop` |
| `ps` | [procs](https://github.com/dalance/procs) | Colored output, tree view | `brew install procs` |
| `du` | [dust](https://github.com/bootandy/dust) | Visual tree, faster | `brew install dust` |
| `man` | [tealdeer](https://github.com/dbrgn/tealdeer) | Simplified examples | `brew install tealdeer` |

### Development Tools

**Version Control**
- [git](https://git-scm.com/) - Distributed version control
- [gh](https://cli.github.com/) - GitHub CLI for PRs and issues
- [lazygit](https://github.com/jesseduffield/lazygit) - Terminal UI for git

**Containerization**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - Container management with GUI
- [Apple Container](https://github.com/apple/container) - Native macOS containers
- [lazydocker](https://github.com/jesseduffield/lazydocker) - Terminal UI for Docker

**Kubernetes**
- [k9s](https://k9scli.io/) - Terminal UI for Kubernetes
- [flux](https://fluxcd.io/) - GitOps continuous delivery

**Text Editors**
- [helix](https://helix-editor.com/) - Modal editor with built-in LSP
- [emacs](https://www.gnu.org/software/emacs/) - Extensible editor
- [Visual Studio Code](https://code.visualstudio.com/) - GUI editor with extensions
- [Cursor](https://cursor.sh/) - AI-first code editor

**Languages & Runtimes**
- [node](https://nodejs.org/) - JavaScript runtime
- [Julia](https://julialang.org/) - Scientific computing language

**Utilities**
- [jq](https://stedolan.github.io/jq/) - JSON processor
- [fzf](https://github.com/junegunn/fzf) - Fuzzy finder
- [glow](https://github.com/charmbracelet/glow) - Markdown renderer
- [wget](https://www.gnu.org/software/wget/) - File downloader

### TUI Applications

| Application | Shortcut | Purpose | Key Commands |
|-------------|----------|---------|--------------|
| yazi | `Ctrl+a f` | File manager | `j/k` nav, `Space` select, `d/y/p` cut/copy/paste |
| helix | `Ctrl+a e` | Text editor | `i` insert, `v` select, `gd` definition, `:w` save |
| lazygit | `Ctrl+a g` | Git interface | `Space` stage, `c` commit, `P` push |
| lazydocker | `Ctrl+a d` | Docker manager | `Space` start/stop, `l` logs, `e` exec |
| k9s | `Ctrl+a k` | Kubernetes | `:pods`, `l` logs, `s` shell |
| atac | `Ctrl+a a` | API client | `Enter` execute, `n` new request |
| procs | `Ctrl+a p` | Process viewer | `c/m` sort CPU/memory, `/` search |
| btop | `Ctrl+a m` | System monitor | Mouse enabled, visual graphs |
| bandwhich | `Ctrl+a n` | Network monitor | Per-process bandwidth usage |
| dust | `Ctrl+a u` | Disk analyzer | Visual directory sizes |
| zellij | `Ctrl+a s` | Session manager | Terminal multiplexer |

### Desktop Applications

**Development**
- iTerm2, WezTerm - Terminal emulators
- GitHub Desktop - Visual Git client
- TeXShop - LaTeX editor

**Security & Privacy**
- 1Password - Password manager with SSH agent
- 1Password CLI - Command-line credential access
- GPG Suite - Email encryption and signing
- ProtonVPN - Privacy-focused VPN

**Productivity**
- Obsidian - Knowledge base and notes
- Raycast - Launcher (replaces Spotlight)
- Zotero - Reference and citation manager
- Claude - AI assistant

**Communication**
- Slack - Team communication
- Signal - Secure messaging
- Telegram - Cloud messaging
- WhatsApp - Personal messaging
- Zoom - Video conferencing

**Browsers**
- Arc - Modern browser with spaces
- Firefox - Privacy-focused browser

**Media**
- Spotify - Music streaming
- VLC - Universal media player
- Sonic Pi - Code-based music creation
- Steam - Gaming platform

### Configuration Management

| Tool | Purpose | Key Commands |
|------|---------|--------------|
| [chezmoi](https://www.chezmoi.io/) | Dotfiles manager | `chezmoi add`, `chezmoi apply`, `chezmoi diff` |
| [starship](https://starship.rs/) | Shell prompt | Configured in `~/.config/starship.toml` |

### AI & ML Tools

| Tool | Purpose | Commands |
|------|---------|----------|
| [llm](https://llm.datasette.io/) | CLI for Large Language Models | `llm "query"`, `llm models` |
| Claude Desktop | AI assistant GUI | Desktop application |

### Security Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| [cosign](https://github.com/sigstore/cosign) | Container signing | `cosign sign`, `cosign verify` |
| GPG Suite | Encryption & signing | `gpg --encrypt`, `gpg --sign` |

## Command Reference

### Essential Commands

**Search & Navigation**
```bash
# Search file contents
rg "pattern"                    # Basic search
rg "pattern" --type=js          # Language-specific
rg "TODO" -C 3                  # Show 3 lines context

# List directories
eza -la                         # Long format with all files
eza --tree                      # Tree view
eza --git                       # Show git status

# Find files
fd "pattern"                    # Simple file search
fd -e js -e ts                  # Find by extension
fd -H "pattern"                 # Include hidden files

# View files
bat filename.py                 # Syntax highlighted view
glow README.md                  # Rendered markdown
```

**File Operations**
```bash
# Copy/move with progress
rsync -av source/ dest/         # Copy with progress
rsync -av --delete src/ dst/    # Sync directories

# Disk usage
dust                            # Visual disk usage
dust -d 2                       # Limit depth to 2 levels
```

**Process Management**
```bash
# View processes
procs                           # Enhanced process list
procs nginx                     # Filter by name
procs --tree                    # Tree view

# System monitoring
btop                            # Interactive system monitor
bandwhich                       # Network usage by process
```

**Package Management**
```bash
# Homebrew
brew install package            # Install package
brew upgrade                    # Upgrade all packages
brew bundle                     # Install from Brewfile
brew bundle cleanup             # Remove unlisted packages

# Python (uv)
uv add package                  # Add dependency
uv run script.py                # Run with environment
uv sync                         # Sync dependencies

# Node.js (pnpm)
pnpm install                    # Install dependencies
pnpm add package                # Add new package
pnpm run script                 # Run package script
```

### Configuration Management (Chezmoi)

**PRIMARY WORKFLOW (HOME → Source)**
```bash
# Edit file in place
vim ~/.zshrc

# Test changes
source ~/.zshrc

# Add to chezmoi
chezmoi add ~/.zshrc

# Commit changes
chezmoi git -- commit -m "feat: add shell configuration"

# Push to remote
chezmoi git -- push
```

**ADVANCED WORKFLOW (Source → HOME)**
```bash
# Edit source directly
chezmoi edit ~/.zshrc

# Preview changes
chezmoi diff

# Apply to HOME
chezmoi apply

# Commit changes
chezmoi git -- commit -m "feat: update shell configuration"
```

**Synchronization**
```bash
chezmoi update                  # Pull latest and apply
chezmoi status                  # Check for changes
chezmoi doctor                  # Diagnose issues
chezmoi diff                    # Review pending changes
```

### Git Operations

**Basic Commands**
```bash
git status                      # Repository status
git add .                       # Stage all changes
git commit -m "message"         # Commit with message
git push                        # Push to remote
git pull                        # Pull from remote
```

**GitHub CLI**
```bash
gh dash                         # GitHub dashboard
gh issue list                   # List issues
gh pr list                      # List pull requests
gh pr create                    # Create pull request
gh repo view                    # View repository info
```

### Network & Testing

**Network Tools**
```bash
speedtest-cli                   # Test bandwidth
wget URL                        # Download file
bandwhich                       # Monitor network per process
```

**Help & Documentation**
```bash
tldr command                    # Simplified man pages
man command                     # Full manual pages
command --help                  # Built-in help
```

### Workspace Commands

```bash
# Launch workspaces
workspace-home                  # Home command center
workspace-dev [project]         # Development workspace
workspace-refresh               # Refresh workspace data

# Session management (zellij)
zellij list-sessions            # Show active sessions
zellij attach session-name      # Reconnect to session
zellij kill-session name        # Terminate session
```

## Keyboard Shortcuts

### WezTerm Leader Key System (Ctrl+a)

The leader key system provides quick access to all tools and workspace management.

**Core TUI Applications**
```
Ctrl+a f     - yazi (file manager)
Ctrl+a e     - helix (text editor)
Ctrl+a g     - lazygit (git interface)
Ctrl+a d     - lazydocker (docker manager)
Ctrl+a k     - k9s (kubernetes)
Ctrl+a a     - atac (API client)
Ctrl+a p     - procs (process viewer)
Ctrl+a m     - btop (system monitor)
Ctrl+a n     - bandwhich (network monitor)
Ctrl+a u     - dust (disk analyzer)
Ctrl+a s     - zellij (session manager)
```

**Workspace Management**
```
Ctrl+a w     - Launch 4-pane development workspace
Ctrl+a h     - Launch home command center
Ctrl+a Shift+W - Launch project workspace
Ctrl+a r     - Refresh current workspace
```

**Pane Management**
```
Ctrl+a |     - Split vertically
Ctrl+a -     - Split horizontally
Ctrl+a h/j/k/l - Navigate to left/down/up/right pane
Ctrl+a Shift+H/J/K/L - Resize pane in direction
Ctrl+a x     - Close current pane (with confirmation)
Ctrl+a z     - Toggle pane fullscreen
```

**WezTerm Native Shortcuts**
```
Cmd+T        - New tab
Cmd+W        - Close tab
Cmd+1-9      - Switch to tab N
Cmd+Shift+[/] - Previous/next tab
Cmd+Enter    - Toggle fullscreen
```

### macOS Text Editing Shortcuts

```
Option + Backspace    - Delete word backward
Cmd + ←/→             - Jump to line start/end
Option + ←/→          - Jump word backward/forward
Cmd + Backspace       - Delete to line start
Option + Delete       - Delete word forward
```

### Application-Specific Shortcuts

**Yazi (File Manager)**
```
j/k          - Move up/down
h/l          - Go back/forward in directories
gg/G         - Go to top/bottom
/            - Search files
Space        - Select/deselect file
d/y/p        - Cut/copy/paste
D            - Delete permanently
r            - Rename file
Tab          - Toggle preview
.            - Toggle hidden files
```

**Helix (Text Editor)**
```
i            - Insert mode
v            - Visual mode (selection)
Esc          - Normal mode
:            - Command mode
h/j/k/l      - Move left/down/up/right
w/b          - Word forward/backward
gg/G         - Start/end of file
d            - Delete selection
y            - Copy (yank)
p            - Paste
u            - Undo
Ctrl+r       - Redo
gd           - Go to definition
gr           - Go to references
K            - Show hover info
Space+f      - File picker
Space+s      - Symbol search
Space+/      - Global search
:w           - Save file
:q           - Quit
```

**Lazygit (Git Interface)**
```
Tab/Shift+Tab - Switch panels
j/k          - Move up/down
Space        - Stage/unstage file
a            - Stage all files
c            - Commit staged changes
P            - Push to remote
p            - Pull from remote
d            - View diff
e            - Edit file
n            - New branch
m            - Merge branch
```

**Lazydocker (Docker Management)**
```
Tab          - Switch panels
j/k          - Move up/down
Space        - Start/stop container
r            - Restart container
s            - Stop container
d            - Delete container
l            - View logs
e            - Exec shell in container
p            - Prune unused resources
```

**K9s (Kubernetes)**
```
:pods        - View pods
:services    - View services
:deployments - View deployments
:nodes       - View nodes
d            - Delete resource
l            - View logs
s            - Shell into pod
Enter        - View details
```

**Procs (Process Monitor)**
```
c            - Sort by CPU
m            - Sort by memory
p            - Sort by PID
n            - Sort by name
/            - Search processes
k            - Kill process
q            - Quit
```

**Atac (API Client)**
```
Tab          - Switch panels
Enter        - Execute request
n            - New request
e            - Edit field
d            - Delete request
```

### Universal Exit Commands

```
q            - Quit most TUI applications
Ctrl+c       - Force quit (universal)
:q           - Vim-style quit (helix)
Ctrl+a x     - Close WezTerm pane
```

## Quick Reference

### Most Common Operations by Workflow

**File Management**
```bash
Ctrl+a f                        # Open file manager
/pattern                        # Search for files
Space (select) → d/y/p          # Cut/copy/paste operations
```

**Code Editing**
```bash
Ctrl+a e                        # Open editor
i (type) → Esc → :w → :q        # Edit, save, quit
gd                              # Jump to definition
Space+f                         # Open file picker
```

**Git Workflow**
```bash
Ctrl+a g                        # Open git interface
Space (stage) → c (commit)      # Stage and commit
P                               # Push changes
```

**Docker Operations**
```bash
Ctrl+a d                        # Open docker manager
Space                           # Start/stop container
l                               # View logs
e                               # Exec into container
```

**System Monitoring**
```bash
Ctrl+a p                        # Process viewer
Ctrl+a m                        # System monitor
Ctrl+a n                        # Network monitor
Ctrl+a u                        # Disk usage
```

**Development Workspace**
```bash
workspace-dev project           # Launch 4-pane layout
Ctrl+a |/-                      # Split panes as needed
Ctrl+a h/j/k/l                  # Navigate between panes
```

**Dotfiles Management**
```bash
vim ~/.config/file              # Edit file in place
source ~/.config/file           # Test changes
chezmoi add ~/.config/file      # Add to chezmoi
chezmoi git -- commit -m "..."  # Commit changes
```

### Configuration File Locations

```
~/.config/
├── starship.toml               # Shell prompt
├── wezterm/wezterm.lua         # Terminal settings
├── helix/config.toml           # Editor configuration
├── yazi/yazi.toml              # File manager settings
├── lazygit/config.yml          # Git UI settings
└── git/config                  # Git configuration

~/.local/bin/                   # Custom scripts
├── workspace-home              # Home workspace launcher
├── workspace-dev               # Dev workspace launcher
└── workspace-refresh           # Workspace refresh

~/.local/share/chezmoi/         # Dotfiles source
└── .git/                       # Dotfiles repository
```

### Environment Variables

```bash
# Chezmoi
CHEZMOI_SOURCE_DIR="$HOME/.local/share/chezmoi"

# Editor
EDITOR="hx"                     # Helix
VISUAL="hx"

# Path
PATH="$HOME/.local/bin:$PATH"   # Custom scripts
```

### Troubleshooting

**Chezmoi Sync Issues**
```bash
chezmoi doctor                  # Diagnose issues
chezmoi status                  # Check changes
chezmoi diff                    # Review pending changes
```

**WezTerm Leader Key Not Working**
- Check if timeout expired (1000ms)
- Verify no conflicting key bindings
- Restart WezTerm if necessary

**TUI Application Crashes**
```bash
reset                           # Reset terminal state
exec zsh                        # Restart shell
```

**Git Authentication Issues**
```bash
ssh-add -l                      # Verify SSH agent
ssh -T git@github.com           # Test GitHub connection
op account list                 # Check 1Password integration
```

**Performance Issues**
```bash
Ctrl+a m                        # Monitor system resources
Ctrl+a n                        # Check network usage
Ctrl+a u                        # Check disk usage
```

**Font Issues**
```bash
# Install required Nerd Font
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font
```

### Learning Path

**Week 1: Core Navigation**
1. File management: `Ctrl+a f` (yazi)
2. Basic editing: `Ctrl+a e` (helix)
3. Git operations: `Ctrl+a g` (lazygit)

**Week 2-3: Development Workflow**
4. Container management: `Ctrl+a d` (lazydocker)
5. Workspace setup: `Ctrl+a w` (4-pane layout)
6. System monitoring: `Ctrl+a p` (procs)

**Week 4+: Advanced Tools**
7. Kubernetes: `Ctrl+a k` (k9s)
8. API testing: `Ctrl+a a` (atac)
9. Network/disk tools: `Ctrl+a n/u` (bandwhich/dust)

---

*For setup instructions → [setup-guide.md](setup-guide.md)*
*For development workflows → [../CLAUDE.md](../CLAUDE.md)*
