#!/bin/bash
# Install Homebrew package manager if not present

set -eufo pipefail

echo "🍺 Checking Homebrew installation..."

if ! command -v brew &> /dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  
  # Add Homebrew to PATH for current session
  if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    echo "✅ Homebrew installed successfully (Apple Silicon)"
  elif [[ -f "/usr/local/bin/brew" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"  
    echo "✅ Homebrew installed successfully (Intel)"
  else
    echo "❌ Homebrew installation may have failed"
    exit 1
  fi
else
  echo "✅ Homebrew is already installed"
fi

# Verify installation
if command -v brew &> /dev/null; then
  echo "✨ Homebrew $(brew --version | head -1) is ready!"
fi