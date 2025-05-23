#!/usr/bin/env bash
#
# Sync iTerm2 Dynamic Profiles from our config directory
# This runs after every chezmoi apply to ensure profiles are up to date

set -euo pipefail

# Source and destination directories
SOURCE_DIR="$HOME/.config/iterm2/DynamicProfiles"
DEST_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Check if source directory exists and has JSON files
if [ -d "$SOURCE_DIR" ] && [ -n "$(find "$SOURCE_DIR" -name "*.json" -type f 2>/dev/null)" ]; then
    echo "🔄 Syncing iTerm2 profiles..."
    
    # Copy all JSON files from source to destination
    # Using rsync to handle updates efficiently
    if command -v rsync >/dev/null 2>&1; then
        rsync -av --delete --include="*.json" --include="*/" --exclude="*" "$SOURCE_DIR/" "$DEST_DIR/"
    else
        # Fallback to cp if rsync isn't available
        cp -f "$SOURCE_DIR"/*.json "$DEST_DIR/"
    fi
    
    echo "✅ iTerm2 profiles synced successfully"
else
    echo "⚠️  No iTerm2 profiles found in $SOURCE_DIR"
fi