#!/usr/bin/env bash
#
# Check what would be migrated to XDG directories
# This is a dry-run version that doesn't move anything

set -euo pipefail

echo "🔍 XDG Migration Check - What would be moved:"
echo "============================================="
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if file/dir exists and where it would go
check_migration() {
    local src="$1"
    local dst="$2"
    local type="$3"
    
    if [ -e "$src" ]; then
        echo -e "${YELLOW}→${NC} $type: ${BLUE}$src${NC}"
        echo -e "  Would move to: ${GREEN}$dst${NC}"
        
        # Check if destination already exists
        if [ -e "$dst" ]; then
            echo -e "  ⚠️  ${YELLOW}Warning: Destination already exists!${NC}"
        fi
        
        # Show size for directories
        if [ -d "$src" ]; then
            local size=$(du -sh "$src" 2>/dev/null | cut -f1)
            echo -e "  Size: $size"
        fi
        echo
    fi
}

# Check current environment variables
echo "📊 Current XDG Environment Variables:"
echo "  XDG_CONFIG_HOME = ${XDG_CONFIG_HOME:-not set (defaults to ~/.config)}"
echo "  XDG_CACHE_HOME = ${XDG_CACHE_HOME:-not set (defaults to ~/.cache)}"
echo "  XDG_DATA_HOME = ${XDG_DATA_HOME:-not set (defaults to ~/.local/share)}"
echo "  XDG_STATE_HOME = ${XDG_STATE_HOME:-not set (defaults to ~/.local/state)}"
echo

# Check what exists in home directory
echo "📁 Configs that would be migrated:"
echo

# Configuration files
check_migration "$HOME/.condarc" "$HOME/.config/conda/condarc" "Conda config"
check_migration "$HOME/.docker" "$HOME/.config/docker" "Docker directory"
check_migration "$HOME/.npmrc" "$HOME/.config/npm/npmrc" "NPM config"
check_migration "$HOME/.ipython" "$HOME/.config/ipython" "IPython directory"
check_migration "$HOME/.jupyter" "$HOME/.config/jupyter" "Jupyter directory"
check_migration "$HOME/.matplotlib" "$HOME/.config/matplotlib" "Matplotlib directory"

# Data directories
check_migration "$HOME/.gnupg" "$HOME/.local/share/gnupg" "GnuPG directory"
check_migration "$HOME/.julia" "$HOME/.local/share/julia" "Julia directory"

# Check for other common dotfiles
echo "📋 Other dotfiles in home (not migrated by script):"
for file in ~/.*; do
    # Skip . and ..
    [ "$file" = "$HOME/." ] || [ "$file" = "$HOME/.." ] && continue
    
    # Skip already checked items
    case "$file" in
        "$HOME/.condarc"|"$HOME/.docker"|"$HOME/.npmrc"|"$HOME/.ipython"|\
        "$HOME/.jupyter"|"$HOME/.matplotlib"|"$HOME/.gnupg"|"$HOME/.julia")
            continue
            ;;
    esac
    
    # Skip essential shell files and XDG directories
    case "$file" in
        "$HOME/.config"|"$HOME/.cache"|"$HOME/.local"|\
        "$HOME/.zshrc"|"$HOME/.zshenv"|"$HOME/.zprofile"|\
        "$HOME/.bashrc"|"$HOME/.bash_profile"|"$HOME/.profile")
            continue
            ;;
    esac
    
    if [ -f "$file" ]; then
        echo "  📄 $(basename "$file")"
    elif [ -d "$file" ]; then
        local size=$(du -sh "$file" 2>/dev/null | cut -f1)
        echo "  📁 $(basename "$file")/ (${size})"
    fi
done

echo
echo "📝 Summary:"
echo "  - The migration script would create proper XDG directory structure"
echo "  - It would move configs to organized locations"
echo "  - Your shell would know where to find them via environment variables"
echo "  - Original files would be moved (not copied)"
echo
echo "💡 To proceed with actual migration, run:"
echo "  ~/.local/share/chezmoi/scripts/migrate-to-xdg.sh"