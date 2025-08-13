# VS Code + Claude Code Integration Setup

## Overview

Comprehensive VS Code configuration integrated with your terminal-first workflow, providing seamless Claude Code access and MCP server integration.

## Files Managed by Chezmoi

### Core Configuration
- `~/.config/Code/User/settings.json` - Main VS Code settings
- `~/.config/Code/User/keybindings.json` - Custom keyboard shortcuts
- `~/.config/Code/User/tasks.json` - Integrated task definitions
- `~/.config/Code/extensions.json` - Recommended extensions list

### Claude Code Integration
- `~/.config/Code/User/claude-mcp.json` - MCP server configuration template
- `~/.local/bin/setup-vscode-claude` - Setup and configuration script

## Key Features

### 1. Terminal Aesthetic Consistency
- **Font**: MesloLGS NF (matches your terminal setup)
- **Theme**: Default Dark Modern (consistent with terminal)
- **Terminal integration**: Uses your zsh setup with proper PATH

### 2. Claude Code Integration
- **Keyboard shortcut**: `Cmd+Esc` launches Claude Code
- **Context sharing**: Current file/selection automatically shared
- **MCP servers**: Same GitHub + HuggingFace integration as terminal

### 3. Workflow Integration
- **Tasks**: Predefined tasks for workspace commands
- **Extensions**: Python, Markdown, Git, AI assistance
- **File management**: Consistent exclude patterns and auto-save

## Setup Process

### 1. Initial Configuration
```bash
# Apply chezmoi configuration
chezmoi apply

# Run VS Code integration setup
~/.local/bin/setup-vscode-claude
```

### 2. MCP Server Setup
The setup script will:
- Resolve 1Password tokens for GitHub/HuggingFace
- Create `claude-mcp-resolved.json` with actual tokens
- Configure VS Code to use the resolved MCP configuration

### 3. Extension Installation
Essential extensions (install manually or via sync):
```bash
code --install-extension github.copilot
code --install-extension github.copilot-chat
code --install-extension ms-python.python
code --install-extension yzhang.markdown-all-in-one
```

## Usage Patterns

### 1. Claude Code Access
- **From VS Code**: Press `Cmd+Esc` to launch Claude Code terminal
- **From Terminal**: Use `code <file>` to open files in VS Code
- **Context**: Current VS Code file/selection automatically shared with Claude

### 2. Workflow Integration
- **Development**: Use `workspace-dev` for terminal-first development
- **Review/Debugging**: Switch to VS Code for complex analysis
- **Documentation**: Markdown editing with enhanced preview

### 3. AI Assistance
- **GitHub Copilot**: Inline suggestions and chat
- **Claude Code**: Full context AI assistant
- **MCP Tools**: GitHub and HuggingFace integration

## Key Shortcuts

### Claude Code Integration
- `Cmd+Esc` - Launch Claude Code
- `Cmd+Shift+C` - Open external terminal

### Navigation & Panels
- `Cmd+P` - Quick file open
- `Cmd+Shift+P` - Command palette
- `Cmd+B` - Toggle sidebar
- `Cmd+J` - Toggle panel
- `Ctrl+`` - Toggle integrated terminal

### AI Assistance
- `Alt+\` - Trigger Copilot suggestions
- `Alt+]` / `Alt+[` - Navigate Copilot suggestions

## Project-Specific Configuration

### Weather-TUI Project
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "uv",
  "python.terminal.activateEnvironment": false
}
```

### Dotfiles Management
- VS Code automatically recognizes chezmoi structure
- Git integration works with both source and target files

## Troubleshooting

### MCP Server Issues
```bash
# Re-run setup to refresh tokens
~/.local/bin/setup-vscode-claude

# Check MCP configuration
cat ~/.config/Code/User/claude-mcp-resolved.json
```

### Claude Code Integration
```bash
# Verify Claude Code CLI
which claude
claude --version

# Test VS Code CLI
which code
code --version
```

### Extension Issues
```bash
# List installed extensions
code --list-extensions

# Force reinstall problematic extension
code --install-extension <extension-id> --force
```

## Security Considerations

### Token Management
- **Source control**: Only template `claude-mcp.json` is versioned
- **Local resolution**: Actual tokens in `claude-mcp-resolved.json`
- **1Password integration**: Tokens retrieved dynamically when possible

### File Exclusions
VS Code is configured to exclude:
- Git directories and files
- Cache directories (`__pycache__`, `.pytest_cache`)
- Temporary files (`.DS_Store`, `*.pyc`)

## Future Enhancements

### Planned Features
- Workspace-specific MCP server configurations
- Custom code snippets for your workflow patterns
- Integration with TaskWarrior for project management

### Extension Recommendations
- GitLens for advanced Git visualization
- Better TOML for configuration files
- Material Icon Theme for better file recognition

---

**Last Updated**: 2025-01-13  
**Chezmoi Files**: All configuration versioned and manageable  
**Status**: Claude Code integration ready, MCP servers configured