# myTUI - Terminal-First Development Environment

*Your personal terminal user interface for modern development*

## Mental Model

**One Terminal Rule All**: Instead of switching between Finder, GitHub Desktop, Docker Desktop, and dozens of other apps, myTUI brings everything into a single terminal interface with instant tool access via leader keys.

**Core Concepts:**
- **Leader Key System** (`Ctrl+a` + key) - Instant access to any tool without context switching
- **Workspace Automation** - Pre-configured 4-pane layouts for different project types  
- **Configuration as Code** - All settings managed via chezmoi dotfiles system
- **AI-Enhanced Development** - Modular memory system with intelligent project context

## What You Get

### Terminal Stack
- **WezTerm** - GPU-accelerated terminal with 120fps rendering
- **Starship** - Fast, informative prompt with git integration
- **Zsh + Prezto** - Advanced shell with intelligent completions

### Tool Ecosystem  
- **File Management** - yazi with image previews and vim navigation
- **Code Editing** - helix with built-in LSP support
- **Git Operations** - lazygit for intuitive git workflows
- **Container Management** - lazydocker replacing Docker Desktop
- **API Testing** - atac as a terminal-based Postman alternative
- **Project Management** - Jira integration with ACLI
- **System Monitoring** - btop, bandwhich, dust for system insights

*See [complete tool reference →](docs/reference.md#tools)*

## Quick Setup

**⏱️ 5 minutes to terminal productivity**

```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Initialize dotfiles
brew install chezmoi
chezmoi init --apply nehalecky/dotfiles

# 3. Install all tools
brew bundle

# 4. Launch home workspace
workspace-home
```

**First Steps:**
1. Press `Ctrl+a f` to open the file manager
2. Press `Ctrl+a e` to open the editor  
3. Press `Ctrl+a g` to see git status
4. Press `Ctrl+a ?` to see all shortcuts

*For detailed setup and troubleshooting → [workflows guide](docs/workflows.md#installation)*

## Daily Usage

### Workspace Management
```bash
workspace-home          # Launch 4-pane home command center
workspace-dev myproject # Launch project-specific development workspace  
```

### Leader Key Shortcuts
Press `Ctrl+a` followed by:
- `f` - File manager (yazi)
- `e` - Editor (helix)  
- `g` - Git interface (lazygit)
- `d` - Docker management (lazydocker)
- `a` - API testing (atac)

*See [complete shortcuts reference →](docs/reference.md#shortcuts)*

### Configuration Management
Your prompt displays dotfiles repository status with visual indicators:

```bash
░▒▓   ~   master ✘?⇡   12:52
#             ↑    ↑↑↑
#        branch  ││└── ahead of remote  
#                │└─── untracked files
#                └──── modified files
```

*Learn more about [configuration workflows →](docs/workflows.md#dotfile-management)*

## Where To Go Next

- **New to this setup?** Continue with [daily workflows →](docs/workflows.md)
- **Need a specific command?** Check the [reference guide →](docs/reference.md) 
- **Something not working?** See [troubleshooting →](docs/workflows.md#troubleshooting)
- **Want to customize?** Learn about [personalization →](docs/workflows.md#customization)

## myTUI Design Philosophy

### Core Design Principles

**1. Cognitive Load Minimization**
- **Single Interface Rule**: All development tools accessible through one terminal interface
- **Consistent Navigation**: Vim-inspired keybindings across all TUI applications
- **Context Preservation**: Mental state maintained through session management and workspace persistence

**2. Performance-First Architecture**
- **Sub-100ms Tool Launch**: Every tool must start in under 100ms for interactive responsability
- **Memory Efficiency**: Prefer Rust/Go implementations over Python/Node.js where performance matters
- **Intelligent Caching**: Session state, command history, and workspace context preserved across restarts

**3. Composable Tool Ecosystem**
- **Best-of-Breed Selection**: Choose the fastest, most feature-complete tool for each function
- **Integration Over Creation**: Compose existing excellent tools rather than building from scratch  
- **Graceful Degradation**: Fallback to traditional tools when modern alternatives unavailable

**4. Configuration Immutability**
- **Declarative Configuration**: All settings defined in version-controlled files
- **Atomic Deployments**: Entire environment reproducible with single command
- **Environment Isolation**: Personal, work, and project-specific configurations cleanly separated

### Problem-Solution Architecture

**Problem**: Context switching between GUI applications destroys flow state
**Solution**: Leader-key system (`Ctrl+a + key`) for instant tool access within single terminal

**Problem**: Inconsistent interfaces across development tools  
**Solution**: TUI applications with unified Vim-inspired navigation patterns

**Problem**: Environment drift and "works on my machine" issues
**Solution**: Chezmoi-managed dotfiles with 1Password secret integration for reproducible environments

**Problem**: Slow tool startup breaking interactive workflows
**Solution**: Performance-optimized tool chain with sub-100ms launch requirements

### Implementation Strategy

**Layer 1: Terminal Foundation**
- WezTerm (GPU acceleration, 120fps rendering)
- Starship (fast prompt with git integration)  
- Zsh + Prezto (intelligent completions)

**Layer 2: TUI Application Suite**
- File Management: `yazi` (image previews, vim navigation)
- Code Editing: `helix` (built-in LSP, modal editing)
- Version Control: `lazygit` (visual git workflows)
- System Monitoring: `btop`, `procs`, `dust` (modern system insights)

**Layer 3: Workflow Automation**
- Workspace Templates: Project-specific 4-panel layouts
- Session Management: Persistent development contexts  
- Configuration Sync: Automatic dotfiles deployment

**Layer 4: AI Integration**
- Context-Aware: Claude Code with project-specific memory modules
- MCP Integrations: GitHub, Google Workspace, Atlassian for seamless API access
- Workflow Intelligence: Automated task management and code analysis

### Claude Code Configuration

This dotfiles repository includes a comprehensive [Claude Code](https://claude.ai/code) configuration with 14 specialized agents, custom hooks, and project-specific memory systems. The setup transforms Claude Code into a powerful development assistant with context-aware workflows and automated tooling.

**Architecture:**
```
~/.claude/                    # Runtime directory (managed by chezmoi)
├── agents/         (14)      # Specialized agents by category
├── hooks/          (9)       # Python workflow automation hooks  
├── memories/       (30+)     # Project context & methodologies
├── commands/       (13)      # Custom slash commands
├── output-styles/  (8)       # Response formatting styles
├── status_lines/   (4)       # Status bar configurations
└── settings.json             # Global configuration
```

**Based on:**
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Original hooks framework
- Custom extensions for consulting and development workflows

**Key Features:**
- **Specialized Agents**: 14 focused agents for development, consulting, research, and platform operations
- **Hook System**: Python hooks for notifications, tool validation, and workflow automation  
- **Memory Modules**: Project-specific context, development methodologies (Discovery-First, Test-Driven, Visual Feedback)
- **MCP Integration**: GitHub, Google Workspace, Atlassian, and Hugging Face API access
- **chezmoi Managed**: All configuration version-controlled and deployable across machines

**Agent Categories:**
- **Development**: repository-manager, system-environment-manager, workflow-designer
- **Consulting**: professional-document-architect, comprehensive-report-generator
- **Research**: client-research-coordinator, confluence-research-agent, llm-ai-agents-and-eng-research
- **Platform**: github-operations-agent, google-workspace-agent, atlas-exec-assistant
- **Utility**: meta-agent, hello-world-agent, work-completion-summary

**Installation:** Run `brew bundle` to install all Claude Code dependencies (fd, ripgrep, marksman, etc.). The configuration is managed directly by chezmoi in `~/.claude/`, with local runtime data excluded from version control via `.chezmoiignore`.

---

**Stack**: WezTerm • Starship • chezmoi • 130+ Modern Tools  
**Approach**: Terminal-native • Security-focused • Performance-optimized