# Conda to UV Migration Reference

## Old Conda Environments

The following conda environments were found and can be recreated with uv if needed:
- birdwatch (Feb 14, 2021)
- empiricstate.com (Feb 16, 2021)
- stat-rethink2-pymc3 (Feb 28, 2021)
- labelops-poc (Nov 29, 2022)

## UV Quick Reference

### Python Version Management
```bash
# Install Python
uv python install 3.12

# List installed Python versions
uv python list

# Use specific Python version for a project
uv python pin 3.12
```

### Virtual Environment Management
```bash
# Create a new virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux

# Create environment with specific Python version
uv venv --python 3.12
```

### Package Management
```bash
# Install packages
uv pip install package-name

# Install from requirements.txt
uv pip install -r requirements.txt

# Create a new project
uv init

# Add dependencies to project
uv add package-name

# Install project dependencies
uv sync
```

### Migrating Conda Environments

To recreate a conda environment with uv:

1. Export conda environment (if still available):
   ```bash
   conda activate old-env
   conda list --export > requirements.txt
   ```

2. Create new uv environment:
   ```bash
   cd project-directory
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

## Next Steps

1. Uninstall miniconda after confirming all projects work with uv:
   ```bash
   brew uninstall miniconda
   ```

2. Clean up conda directories:
   ```bash
   rm -rf ~/.conda
   rm -rf ~/.condarc
   ```