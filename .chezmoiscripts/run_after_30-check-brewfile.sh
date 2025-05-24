#!/bin/bash
# Check and sync Brewfile after chezmoi apply

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🍺 Checking Homebrew state..."

# Generate current Brewfile
TEMP_BREWFILE=$(mktemp)
brew bundle dump --file="$TEMP_BREWFILE" --force --describe

# Compare with managed Brewfile
if ! diff -q Brewfile "$TEMP_BREWFILE" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC}  Brewfile is out of sync with installed packages!"
    echo
    echo "Changes detected:"
    diff -u Brewfile "$TEMP_BREWFILE" | grep "^[+-]" | grep -v "^[+-]{3}" | head -20 || true
    echo
    read -p "Update Brewfile to match current system? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Copy the new Brewfile
        cp "$TEMP_BREWFILE" Brewfile
        
        # Add to chezmoi
        chezmoi add Brewfile
        
        echo -e "${GREEN}✓${NC} Brewfile updated!"
        echo
        echo -e "${BLUE}ℹ${NC}  Next steps:"
        echo "   1. Review changes: chezmoi diff"
        echo "   2. Commit when ready: chezmoi git add Brewfile && chezmoi git commit"
    else
        echo
        echo -e "${BLUE}ℹ${NC}  To manually sync later:"
        echo "   brew bundle dump --force --describe && chezmoi add Brewfile"
    fi
else
    echo -e "${GREEN}✓${NC} Brewfile is in sync"
fi

rm -f "$TEMP_BREWFILE"