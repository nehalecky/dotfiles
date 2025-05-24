#!/usr/bin/env bash
#
# Migrate from Miniconda to uv
# This script helps clean up conda and set up uv

set -euo pipefail

echo "🚀 Python Migration: Miniconda → uv"
echo "==================================="
echo

# Step 1: Check current status
echo "📊 Current Python Setup:"
if command -v conda >/dev/null 2>&1; then
    echo "  ✓ Conda is installed"
    conda_envs=$(conda env list | grep -v "^#" | grep -v "^base" | wc -l)
    echo "  → Found $conda_envs conda environments"
else
    echo "  ✗ Conda not found in PATH"
fi

# List Python versions
echo -e "\n  Python versions:"
brew list | grep "^python@" | while read -r ver; do
    echo "    - $ver (via Homebrew)"
done

# Step 2: Install uv if not present
if ! command -v uv >/dev/null 2>&1; then
    echo -e "\n📦 Installing uv..."
    echo "Please run: brew install uv"
else
    echo -e "\n✓ uv is already installed: $(uv --version)"
fi

# Step 3: Backup conda environments (if any)
if command -v conda >/dev/null 2>&1; then
    echo -e "\n💾 Backing up conda environments..."
    mkdir -p ~/.config/python/conda-backup
    conda env list --json > ~/.config/python/conda-backup/environments.json
    echo "  → Saved environment list to ~/.config/python/conda-backup/"
fi

# Step 4: Create cleanup checklist
echo -e "\n🧹 Cleanup Checklist:"
echo "══════════════════════"
echo
echo "1. Uninstall Miniconda:"
echo "   brew uninstall --cask miniconda"
echo
echo "2. Remove conda directories:"
echo "   rm -rf ~/miniconda3"
echo "   rm -rf ~/.conda"
echo "   rm -rf ~/.config/conda"  # Our XDG location
echo
echo "3. Clean shell configuration:"
echo "   Remove conda initialization from ~/.zshrc"
echo "   (between >>> conda initialize >>> and <<< conda initialize <<<)"
echo
echo "4. Install uv (if not done):"
echo "   brew install uv"
echo
echo "5. Set up uv for your projects:"
echo "   cd your-project"
echo "   uv venv                    # Create virtual environment"
echo "   source .venv/bin/activate  # Activate it"
echo "   uv pip install -r requirements.txt"
echo

# Step 5: Configure XDG for uv
echo "📁 Setting up XDG directories for uv..."
mkdir -p ~/.cache/uv
mkdir -p ~/.local/share/uv

echo -e "\n✅ Migration preparation complete!"
echo
echo "📝 uv advantages over conda:"
echo "  • 10-100x faster package resolution"
echo "  • No base environment pollution"
echo "  • Simpler, cleaner design"
echo "  • Better pip compatibility"
echo "  • Smaller disk footprint"