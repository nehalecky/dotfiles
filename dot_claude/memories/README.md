# Claude Code Memory System

## Overview

This directory contains a modular memory system for Claude Code that leverages the @import functionality to provide organized, reusable development context across all projects.

## Architecture

```
~/.claude/memories/
├── workflows/           # Core development methodologies
│   ├── core-workflows.md       # Main workflow coordinator
│   ├── discovery-first.md      # Complex/unfamiliar codebase workflow
│   ├── test-driven.md          # Clear requirements workflow
│   └── visual-feedback.md      # UI/UX development workflow
├── tools/              # Essential tooling and practices
│   ├── chezmoi.md             # Dotfiles management patterns
│   ├── git-practices.md       # Git workflows and conventions
│   ├── essential-tools.md     # Modern CLI tool preferences
│   └── tui-workflows.md       # Terminal UI and workspace management
├── stacks/             # Technology-specific patterns
│   ├── python.md              # Python development with UV, pytest, ruff
│   ├── nodejs.md              # Node.js/TypeScript development
│   └── web-frontend.md        # React/Vue frontend development
├── mcp/                # MCP server integrations
│   ├── installation.md       # General MCP installation patterns
│   ├── github-integration.md # GitHub MCP workflows
│   └── huggingface-integration.md # Hugging Face MCP workflows
└── templates/          # Project template generation
    └── generator.py           # Smart CLAUDE.md generator
```

## How It Works

### Import Chain System

The system uses Claude Code's @import syntax to create hierarchical memory chains:

1. **Global CLAUDE.md** imports core modules
2. **Core modules** import specific implementations  
3. **Project CLAUDE.md** files import relevant global modules
4. **Maximum 5-hop import depth** maintained for performance

### Example Import Chain

```
Project CLAUDE.md
└── @.claude/memories/workflows/core-workflows.md
    ├── @discovery-first.md
    ├── @test-driven.md
    └── @visual-feedback.md
```

## Usage

### For New Projects

Generate a smart CLAUDE.md file with automatic project detection:

```bash
# Generate for current directory
python3 ~/.claude/memories/templates/generator.py .

# Generate for specific project
python3 ~/.claude/memories/templates/generator.py /path/to/project

# Generate with custom output path
python3 ~/.claude/memories/templates/generator.py /path/to/project /custom/output.md
```

### What the Generator Detects

- **Project Type**: Python, Node.js, Web Frontend, Rust, Go, Mixed, Unknown
- **Package Files**: pyproject.toml, package.json, Cargo.toml, etc.
- **Testing Setup**: pytest, Jest, Vitest configurations
- **CI/CD**: GitHub Actions, GitLab CI, etc.
- **Technology Stack**: Specific frameworks and tools in use

### Automatic Import Selection

The generator automatically includes relevant imports:

| Project Type | Includes |
|--------------|----------|
| Python | python.md, essential-tools.md, git-practices.md |
| Node.js | nodejs.md, essential-tools.md, git-practices.md |
| Web Frontend | nodejs.md, web-frontend.md, essential-tools.md |
| Mixed | Multiple stack modules as detected |
| Git Repository | github-integration.md (if applicable) |

## Memory Modules

### Workflows (`/workflows/`)

**Core development methodologies for different scenarios:**

- **discovery-first.md** - For complex features or unfamiliar codebases
- **test-driven.md** - For new functionality with clear requirements  
- **visual-feedback.md** - For UI/UX development and visual outputs

### Tools (`/tools/`)

**Essential tooling and workflow patterns:**

- **chezmoi.md** - Dotfiles management with HOME→Source workflow enforcement
- **git-practices.md** - Git conventions, commit messages, branching strategies
- **essential-tools.md** - Modern CLI tool preferences (rg, eza, bat, etc.)
- **tui-workflows.md** - Terminal UI applications and workspace management

### Stacks (`/stacks/`)

**Technology-specific development patterns:**

- **python.md** - UV package management, pytest, ruff, mypy integration
- **nodejs.md** - npm/pnpm, TypeScript, ESLint, testing frameworks
- **web-frontend.md** - React/Vue, Vite, component patterns, performance

### MCP Integrations (`/mcp/`)

**Model Context Protocol server integrations:**

- **installation.md** - General MCP server setup and troubleshooting
- **github-integration.md** - Repository management, issues, PRs, actions
- **huggingface-integration.md** - Model/dataset search, research workflows

## Maintenance

### Adding New Modules

1. Create new .md file in appropriate directory
2. Follow existing naming conventions
3. Include proper @import statements if needed
4. Update this README.md with new module description
5. Test imports work correctly
6. Commit to chezmoi: `chezmoi add ~/.claude/memories/`

### Updating Existing Modules

1. Edit module files directly in `~/.claude/memories/`
2. Changes propagate automatically to all importing projects
3. Commit changes: `chezmoi git -- commit -m "update: memory module changes"`

### Version Control

The memory system is managed through chezmoi for cross-machine synchronization:

```bash
# Add new modules
chezmoi add ~/.claude/memories/

# Commit changes
chezmoi git -- commit -m "feat: add new memory module"

# Sync across machines
chezmoi update
```

## Benefits

### For Development

- **Consistent Patterns** - Standardized workflows across all projects
- **Reduced Duplication** - Shared knowledge instead of repeated instructions
- **Smart Setup** - Projects automatically get relevant context
- **Easy Updates** - Change once, propagate everywhere

### For Memory Management

- **Organized Structure** - Logical hierarchy instead of monolithic files
- **Import Efficiency** - Only load relevant context for each project
- **Maintainable** - Easy to update and extend individual components
- **Version Controlled** - Full history and cross-machine sync

## Troubleshooting

### Import Chain Issues

If imports aren't working:

1. Check file paths in @import statements
2. Verify files exist in expected locations
3. Ensure proper relative path syntax
4. Test with simple imports first

### Generator Issues

If the project generator fails:

1. Verify Python 3 is available
2. Check project path exists and is readable
3. Ensure write permissions for output location
4. Run with verbose error output

### Missing Modules

If specific modules aren't found:

1. Check `~/.claude/memories/` directory structure
2. Verify chezmoi has latest version: `chezmoi update`
3. Re-run generator to update project imports
4. Check file permissions

## Migration Guide

### From Monolithic CLAUDE.md

If you have existing monolithic CLAUDE.md files:

1. **Backup existing files**: `cp CLAUDE.md CLAUDE.md.backup`
2. **Run generator**: `python3 ~/.claude/memories/templates/generator.py .`
3. **Review generated output** and merge any custom content
4. **Test import chain** works correctly
5. **Commit changes** to version control

### From Manual Templates

Replace manual template usage with the smart generator:

1. **Delete old template files** (if any)
2. **Use generator for new projects**
3. **Update existing projects** with regenerated CLAUDE.md files
4. **Document project-specific customizations** that need preservation

## Contributing

### Adding New Technology Stacks

1. Create new file in `/stacks/` directory
2. Follow existing patterns for structure and content
3. Include setup, development, testing, and deployment patterns
4. Add integration with essential tools
5. Update generator.py to detect the new stack
6. Test with sample projects

### Improving Existing Modules

1. Follow established patterns and conventions
2. Maintain backward compatibility with existing imports
3. Add clear documentation for any breaking changes
4. Test changes across multiple project types
5. Update related modules if dependencies change

---

*This modular memory system provides intelligent, organized development context while maintaining the critical workflow enforcement and session patterns essential for productive Claude Code usage.*