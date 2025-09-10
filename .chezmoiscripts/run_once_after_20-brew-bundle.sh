#!/bin/bash
# Install all packages from Brewfile after Homebrew is available

set -eufo pipefail

echo "📦 Installing packages from Brewfile..."

# Ensure Homebrew is in PATH
if command -v brew &> /dev/null; then
  echo "✅ Homebrew found, proceeding with package installation"
else
  echo "❌ Homebrew not found in PATH, attempting to add it..."
  if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -f "/usr/local/bin/brew" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  else
    echo "❌ Cannot find Homebrew installation"
    exit 1
  fi
fi

# Check if Brewfile exists
if [[ -f "$HOME/.Brewfile" ]]; then
  echo "📋 Found Brewfile, installing packages..."
  cd "$HOME"
  brew bundle --no-lock
  echo "✅ All packages installed successfully"
else
  echo "❌ Brewfile not found at $HOME/.Brewfile"
  echo "💡 Brewfile should be deployed before this script runs"
  exit 1
fi

# Verify key tools are installed
echo "🔍 Verifying essential tools..."
essential_tools=(
  "rg"
  "fd" 
  "eza"
  "bat"
  "delta"
  "yazi"
  "helix"
  "lazygit"
  "gh"
  "glow"
)

missing=0
for tool in "${essential_tools[@]}"; do
  if command -v "$tool" &> /dev/null; then
    echo "✅ $tool available"
  else
    echo "❌ $tool not found"
    ((missing++))
  fi
done

if [[ $missing -eq 0 ]]; then
  echo "✨ All essential development tools are ready!"
else
  echo "⚠️  $missing essential tools are missing"
fi