#!/usr/bin/env bash
#
# Migrate dotfiles to XDG-compliant locations
# This script helps move configs from ~ to ~/.config

set -euo pipefail

echo "🚀 Starting XDG migration..."

# Function to safely move files
move_if_exists() {
    local src="$1"
    local dst="$2"
    
    if [ -e "$src" ]; then
        # Create destination directory
        mkdir -p "$(dirname "$dst")"
        
        # Check if destination exists
        if [ -e "$dst" ]; then
            echo "⚠️  Destination exists: $dst (skipping)"
        else
            echo "📦 Moving: $src → $dst"
            mv "$src" "$dst"
        fi
    fi
}

# 1. Conda
if [ -f "$HOME/.condarc" ]; then
    echo "🐍 Migrating Conda config..."
    move_if_exists "$HOME/.condarc" "$HOME/.config/conda/condarc"
fi

# 2. Docker
if [ -d "$HOME/.docker" ]; then
    echo "🐳 Migrating Docker config..."
    move_if_exists "$HOME/.docker" "$HOME/.config/docker"
fi

# 3. NPM
if [ -f "$HOME/.npmrc" ]; then
    echo "📦 Migrating NPM config..."
    move_if_exists "$HOME/.npmrc" "$HOME/.config/npm/npmrc"
fi

# 4. Create minimal .gitconfig that includes the real config
if [ -f "$HOME/.gitconfig" ] && [ ! -f "$HOME/.config/git/config" ]; then
    echo "🔧 Setting up Git config redirect..."
    mkdir -p "$HOME/.config/git"
    cp "$HOME/.gitconfig" "$HOME/.config/git/config"
    cat > "$HOME/.gitconfig" << 'EOF'
# This file redirects to the actual config in ~/.config/git/config
# Maintained by chezmoi
[include]
    path = ~/.config/git/config
EOF
fi

# 5. IPython/Jupyter
if [ -d "$HOME/.ipython" ]; then
    echo "🔬 Migrating IPython config..."
    move_if_exists "$HOME/.ipython" "$HOME/.config/ipython"
fi

if [ -d "$HOME/.jupyter" ]; then
    echo "📓 Migrating Jupyter config..."
    move_if_exists "$HOME/.jupyter" "$HOME/.config/jupyter"
fi

# 6. Create directory structure
echo "📁 Creating XDG directory structure..."
mkdir -p "$HOME/.config"/{shell,git,npm,conda,docker}
mkdir -p "$HOME/.cache"/{pip,yarn,less,pylint}
mkdir -p "$HOME/.local/share"/{gnupg,virtualenvs,gem,cargo}
mkdir -p "$HOME/.local/state/zsh"

echo "✅ XDG migration complete!"
echo ""
echo "📝 Next steps:"
echo "1. Source your shell: source ~/.zshrc"
echo "2. Test your applications"
echo "3. Add configs to chezmoi: chezmoi add ~/.config/"
echo ""
echo "💡 Your home directory is now cleaner!"