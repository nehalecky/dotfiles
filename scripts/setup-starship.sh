#!/bin/bash
# Setup script for migrating from Powerlevel10k to Starship

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starship Migration Setup${NC}"
echo

# Check if Starship is installed
if ! command -v starship &> /dev/null; then
    echo -e "${YELLOW}Starship not found. Installing...${NC}"
    brew install starship
else
    echo -e "${GREEN}✓ Starship is already installed${NC}"
fi

# Backup P10k config if not already done
if [[ -f ~/.p10k.zsh ]] && [[ ! -f ~/.p10k.zsh.backup ]]; then
    echo "Backing up Powerlevel10k configuration..."
    cp ~/.p10k.zsh ~/.p10k.zsh.backup
    echo -e "${GREEN}✓ P10k config backed up${NC}"
fi

# Show current prompt info
echo
echo -e "${BLUE}Current Setup:${NC}"
echo "- Shell: $SHELL"
echo "- Prompt: Powerlevel10k"
echo

# Offer to test Starship temporarily
echo -e "${YELLOW}Would you like to:${NC}"
echo "1) Test Starship temporarily (just for this session)"
echo "2) Switch to Starship permanently"
echo "3) Show comparison of both prompts"
echo "4) Exit"
echo
read -p "Choice (1-4): " choice

case $choice in
    1)
        echo
        echo -e "${BLUE}Testing Starship for this session only...${NC}"
        echo "Your .zshrc remains unchanged. Start a new terminal to go back to P10k."
        echo
        eval "$(starship init zsh)"
        ;;
    
    2)
        echo
        echo -e "${BLUE}Switching to Starship permanently...${NC}"
        
        # Create a modified .zshrc
        cp ~/.zshrc ~/.zshrc.starship
        
        # Comment out P10k lines and add Starship
        sed -i '' '/# Enable Powerlevel10k/,/source ~\/.p10k.zsh/s/^/# /' ~/.zshrc.starship
        
        # Add Starship init
        echo "" >> ~/.zshrc.starship
        echo "# Starship prompt" >> ~/.zshrc.starship
        echo 'eval "$(starship init zsh)"' >> ~/.zshrc.starship
        
        echo -e "${GREEN}✓ Created ~/.zshrc.starship${NC}"
        echo
        echo "To complete the switch:"
        echo "  mv ~/.zshrc ~/.zshrc.p10k"
        echo "  mv ~/.zshrc.starship ~/.zshrc"
        echo "  source ~/.zshrc"
        echo
        echo "To revert:"
        echo "  mv ~/.zshrc.p10k ~/.zshrc"
        echo "  source ~/.zshrc"
        ;;
    
    3)
        echo
        echo -e "${BLUE}Prompt Comparison:${NC}"
        echo
        echo "Powerlevel10k:"
        echo "  ╭─ os_icon + directory + git_status          time + context"
        echo "  ╰─❯ (your command here)"
        echo
        echo "Starship (with our config):"
        echo "  hostname + directory + git_status + python_env"
        echo "  ❯ (your command here)                        duration + time"
        echo
        echo "Key differences:"
        echo "- Starship auto-detects language versions in projects"
        echo "- Simpler configuration (TOML vs Zsh)"
        echo "- Cross-shell compatible"
        echo "- Shows command duration on the right"
        ;;
    
    4)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac