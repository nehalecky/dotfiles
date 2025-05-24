#!/bin/sh
# Install 1Password CLI if not present
# Reference: https://www.chezmoi.io/user-guide/advanced/install-your-password-manager-on-init/

set -e

# Check if 1Password CLI is already installed
if command -v op >/dev/null 2>&1; then
    echo "1Password CLI already installed"
    exit 0
fi

echo "Installing 1Password CLI..."

case "$(uname -s)" in
    Darwin)
        # macOS installation via Homebrew
        if command -v brew >/dev/null 2>&1; then
            brew install --cask 1password-cli
        else
            echo "Error: Homebrew not found. Please install Homebrew first."
            exit 1
        fi
        ;;
    Linux)
        # Linux installation would go here
        echo "Linux installation not yet implemented"
        exit 1
        ;;
    *)
        echo "Unsupported operating system: $(uname -s)"
        exit 1
        ;;
esac

echo "1Password CLI installed successfully"