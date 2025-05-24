#!/bin/bash
# Sync secrets from 1Password to encrypted files for fallback
# This maintains 1Password as the canonical source while enabling
# deployment to environments without 1Password access

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔐 Syncing secrets from 1Password to encrypted fallback files..."

# Check prerequisites
if ! command -v op &> /dev/null; then
    echo -e "${RED}Error: 1Password CLI (op) not found${NC}"
    echo "Install with: brew install --cask 1password-cli"
    exit 1
fi

if ! command -v age &> /dev/null; then
    echo -e "${YELLOW}Warning: age not found, installing...${NC}"
    brew install age
fi

# Ensure we're in chezmoi source directory
CHEZMOI_SOURCE=$(chezmoi source-path)
cd "$CHEZMOI_SOURCE"

# Create secrets directory if it doesn't exist
mkdir -p .secrets

# Sign in to 1Password (will prompt if needed)
if ! op account list &> /dev/null; then
    echo "Please sign in to 1Password..."
    eval $(op signin)
fi

# Define secrets to sync
# Format: "filename:1password-reference"
declare -a SECRETS=(
    # Example entries - uncomment and modify as needed:
    # "github-token:op://Personal/GitHub/personal-access-token"
    # "openai-key:op://Personal/OpenAI/api-key"
    # "aws-access-key:op://Work/AWS/access-key-id"
    # "aws-secret-key:op://Work/AWS/secret-access-key"
)

# Counter for results
synced=0
failed=0

# Sync each secret
for entry in "${SECRETS[@]}"; do
    IFS=':' read -r filename op_ref <<< "$entry"
    
    echo -n "Syncing $filename... "
    
    if op read "$op_ref" 2>/dev/null | age --encrypt --armor > ".secrets/${filename}.age"; then
        echo -e "${GREEN}✓${NC}"
        ((synced++))
    else
        echo -e "${RED}✗ Failed${NC}"
        echo -e "${RED}  Could not read from: $op_ref${NC}"
        ((failed++))
    fi
done

# Summary
echo
echo "Sync complete:"
echo -e "  ${GREEN}✓ Synced: $synced${NC}"
if [ $failed -gt 0 ]; then
    echo -e "  ${RED}✗ Failed: $failed${NC}"
else
    echo -e "  ${GREEN}✓ All secrets synced successfully!${NC}"
fi

# Reminder
if [ $synced -gt 0 ]; then
    echo
    echo "📝 Next steps:"
    echo "1. Test decryption: cat .secrets/FILENAME.age | age --decrypt"
    echo "2. Add to git: chezmoi git add .secrets/"
    echo "3. Commit: chezmoi git commit -m 'Update encrypted secrets'"
fi