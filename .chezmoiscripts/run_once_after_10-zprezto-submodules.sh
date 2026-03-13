#!/bin/bash
# Initialize zprezto git submodules after chezmoi deploys the repo.
#
# The .chezmoiexternal.yaml clones zprezto via chezmoi's git-repo external type,
# but submodule initialization is not guaranteed on all chezmoi versions.
# This script ensures syntax-highlighting and history-substring-search submodules
# are always populated, preventing shell startup errors on fresh installs.
#
# Fixes: https://github.com/nehalecky/dotfiles/issues/5

set -euo pipefail

ZPREZTO="${ZDOTDIR:-$HOME}/.zprezto"

if [[ ! -d "$ZPREZTO" ]]; then
  echo "zprezto not found at $ZPREZTO, skipping submodule init"
  exit 0
fi

if [[ ! -f "$ZPREZTO/.gitmodules" ]]; then
  echo "No .gitmodules found in $ZPREZTO, skipping submodule init"
  exit 0
fi

echo "Initializing zprezto submodules..."
cd "$ZPREZTO"
git submodule update --init --recursive
echo "zprezto submodules initialized"
