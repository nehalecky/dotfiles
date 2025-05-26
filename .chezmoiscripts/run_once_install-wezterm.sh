#!/bin/bash
# Install WezTerm terminal emulator

set -eufo pipefail

echo "🖥️  Checking WezTerm installation..."

if ! command -v wezterm &> /dev/null; then
  echo "Installing WezTerm..."
  brew install --cask wezterm
  echo "✅ WezTerm installed successfully"
else
  echo "✅ WezTerm is already installed"
fi

# Verify installation
if command -v wezterm &> /dev/null; then
  echo "✨ WezTerm $(wezterm --version) is ready!"
fi