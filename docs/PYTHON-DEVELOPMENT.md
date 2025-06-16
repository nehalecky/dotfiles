# Python Development with uv

This document covers the modern Python development workflow using [uv](https://docs.astral.sh/uv/) as the primary package manager and virtual environment tool.

## Overview

**uv** is an extremely fast Python package installer and resolver written in Rust. It serves as a drop-in replacement for pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more.

**Migration Status**: ✅ **Complete** - Migrated from conda/miniconda to uv in May 2025

## Key Features

- **Blazingly fast**: 10-100x faster than pip
- **Drop-in replacement**: Compatible with pip and requirements.txt
- **Project management**: Built-in virtual environment and dependency management
- **Python installation**: Can install and manage Python versions
- **Cross-platform**: Works on macOS, Linux, and Windows

## Installation

uv is installed via Homebrew in our setup:
```bash
brew install uv
```

## Project Workflow

### Creating a New Project

```bash
# Create new project directory
mkdir my-project && cd my-project

# Initialize uv project (creates pyproject.toml and .python-version)
uv init

# Add dependencies
uv add requests pandas

# Add development dependencies
uv add --dev pytest black ruff
```

### Working with Existing Projects

```bash
# Clone and setup
git clone https://github.com/user/project.git
cd project

# Install dependencies (creates .venv automatically)
uv sync

# Run commands in the project environment
uv run python script.py
uv run pytest
```

## Virtual Environment Management

### Manual Activation (Current Workflow)

```bash
# Create virtual environment
uv venv

# Activate (manual)
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Deactivate
deactivate
```

### Project-Based Commands (Recommended)

```bash
# Run in project environment without activation
uv run python script.py
uv run pytest
uv run jupyter notebook

# Add new packages
uv add numpy scipy

# Remove packages
uv remove old-package
```

## Automatic Environment Activation

**Current Status**: ⚠️ **Manual Setup Required**

uv doesn't provide built-in automatic virtual environment activation when entering directories. Here are the available options:

### Option 1: Using direnv (Recommended)

Install direnv for automatic environment activation:

```bash
brew install direnv
```

Add to your shell configuration (already in our .zshrc):
```bash
eval "$(direnv hook zsh)"
```

Create `.envrc` in your project:
```bash
# For uv projects
echo "source .venv/bin/activate" > .envrc
direnv allow
```

**Alternative with UV_PROJECT_ENVIRONMENT**:
```bash
# Use custom venv location
echo "export UV_PROJECT_ENVIRONMENT=~/.virtualenvs/$(basename $PWD)" > .envrc
direnv allow
```

### Option 2: Custom Shell Hook

Add to `.zshrc` for automatic activation:
```bash
# Auto-activate uv virtual environments
autoload -U add-zsh-hook

_uv_auto_activate() {
    if [[ -f ".venv/bin/activate" ]]; then
        if [[ "$VIRTUAL_ENV" != "$PWD/.venv" ]]; then
            source .venv/bin/activate
        fi
    elif [[ -n "$VIRTUAL_ENV" && "$PWD" != "$VIRTUAL_ENV"* ]]; then
        deactivate
    fi
}

add-zsh-hook chpwd _uv_auto_activate
_uv_auto_activate  # Run on shell start
```

### Option 3: Using uv run (No Activation Needed)

The simplest approach - use `uv run` for all commands:
```bash
# No activation needed - uv handles the environment
uv run python -c "import requests; print('works!')"
uv run pytest
uv run jupyter lab
```

## Python Version Management

```bash
# List available Python versions
uv python list

# Install specific Python version
uv python install 3.11

# Set project Python version
echo "3.11" > .python-version

# Use specific Python for project
uv venv --python 3.11
```

## Common Commands

### Package Management
```bash
# Add package
uv add package-name

# Add dev dependency
uv add --dev pytest

# Add with version constraint
uv add "django>=4.0,<5.0"

# Remove package
uv remove package-name

# Update all packages
uv sync --upgrade

# Show dependencies
uv tree
```

### Environment Commands
```bash
# Create virtual environment
uv venv

# Create with specific Python
uv venv --python 3.11

# Create in custom location
uv venv /path/to/venv

# Remove virtual environment
rm -rf .venv
```

### Running Code
```bash
# Run Python script
uv run python script.py

# Run with specific Python
uv run --python 3.11 python script.py

# Run installed tool
uv run black .
uv run pytest

# Install and run tool temporarily
uv tool run ruff check .
```

## Project Structure

A typical uv project structure:
```
my-project/
├── .python-version          # Python version (e.g., "3.11")
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Lockfile with exact versions
├── .venv/                   # Virtual environment (auto-created)
├── src/                     # Source code
└── tests/                   # Test files
```

## Integration with Other Tools

### With VS Code
VS Code automatically detects `.venv` directories and offers to use them as the Python interpreter.

### With Jupyter
```bash
# Install jupyter in project
uv add jupyter

# Run jupyter (uses project environment)
uv run jupyter lab
```

### With Pre-commit
```bash
# Add pre-commit hooks
uv add --dev pre-commit

# Setup hooks
uv run pre-commit install

# Run hooks
uv run pre-commit run --all-files
```

## Troubleshooting

### Environment Not Found
```bash
# Recreate environment
rm -rf .venv
uv sync
```

### Package Installation Issues
```bash
# Clear cache and reinstall
uv cache clean
uv sync --reinstall
```

### Python Version Issues
```bash
# Check available versions
uv python list

# Install missing version
uv python install 3.11

# Verify project Python
uv run python --version
```

## Migration from conda

If you have old conda environments, you can recreate them with uv:

```bash
# Export conda environment
conda env export > environment.yml

# Create requirements.txt from conda export
# (manual conversion needed)

# Install with uv
uv add package1 package2 package3
```

## Performance Benefits

**Speed Comparisons** (installing packages):
- **pip**: ~45 seconds
- **poetry**: ~60 seconds  
- **uv**: ~2 seconds

**Disk Usage**:
- **conda**: ~500MB per environment
- **virtualenv**: ~20MB per environment
- **uv**: ~15MB per environment

## Best Practices

1. **Use `uv run` for everything** - Avoid manual activation when possible
2. **Pin Python versions** - Always include `.python-version` in projects
3. **Commit lock files** - Include `uv.lock` in version control
4. **Use project mode** - Prefer `uv init` over manual setup
5. **Leverage caching** - uv automatically caches packages for faster installs

## See Also

- **[APPLICATIONS.md](APPLICATIONS.md)** - Complete list of development tools including uv
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture showing Python tooling integration
- **[claude-code-emacs-guide.md](claude-code-emacs-guide.md)** - AI-assisted Python development in Emacs

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [Python Project Guide](https://docs.astral.sh/uv/guides/projects/)
- [Migration from other tools](https://docs.astral.sh/uv/guides/integration/)

---

*This workflow provides a modern, fast, and reliable Python development experience while maintaining compatibility with existing Python tooling.*