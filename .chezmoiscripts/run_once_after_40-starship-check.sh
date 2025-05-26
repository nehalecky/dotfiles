#!/bin/bash
# Check if user wants to try Starship

# Only run if we're still using P10k
if grep -q "Enable Powerlevel10k" ~/.zshrc 2>/dev/null && ! grep -q "# Enable Powerlevel10k" ~/.zshrc 2>/dev/null; then
    if command -v starship &> /dev/null; then
        echo
        echo "🚀 Starship is installed! You're currently using Powerlevel10k."
        echo "   Run 'setup-starship.sh' to try Starship or migrate."
        echo
    fi
fi