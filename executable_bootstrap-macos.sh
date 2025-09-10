#!/bin/bash
# 
# Bootstrap Script for Nicholaus Eugene Halecky's Development Environment
# Transforms bare macOS into complete terminal-first development setup
#
# Usage: curl -fsSL https://raw.githubusercontent.com/nehalecky/dotfiles/master/bootstrap-macos.sh | bash
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_section() { echo -e "${PURPLE}[SECTION]${NC} $1"; }

# Configuration
DOTFILES_REPO="https://github.com/nehalecky/dotfiles.git"
HOMEBREW_URL="https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"

# System requirements check
check_system() {
    log_section "System Requirements Check"
    
    if [[ "$(uname -s)" != "Darwin" ]]; then
        log_error "This script is designed for macOS only"
        exit 1
    fi
    
    log_info "macOS detected: $(sw_vers -productVersion)"
    
    # Check if Xcode Command Line Tools are installed
    if ! xcode-select -p &> /dev/null; then
        log_info "Installing Xcode Command Line Tools..."
        xcode-select --install
        log_warning "Please complete the Xcode Command Line Tools installation and re-run this script"
        exit 1
    fi
    
    log_success "Xcode Command Line Tools are installed"
}

# Install Homebrew
install_homebrew() {
    log_section "Installing Homebrew Package Manager"
    
    if command -v brew &> /dev/null; then
        log_info "Homebrew already installed at: $(which brew)"
        return
    fi
    
    log_info "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL $HOMEBREW_URL)"
    
    # Add Homebrew to PATH for this session
    eval "$(/opt/homebrew/bin/brew shellenv)"
    
    log_success "Homebrew installed successfully"
}

# Install chezmoi
install_chezmoi() {
    log_section "Installing chezmoi Configuration Manager"
    
    if command -v chezmoi &> /dev/null; then
        log_info "chezmoi already installed: $(chezmoi --version)"
        return
    fi
    
    log_info "Installing chezmoi via Homebrew..."
    brew install chezmoi
    
    log_success "chezmoi installed successfully"
}

# Initialize dotfiles
setup_dotfiles() {
    log_section "Setting Up Dotfiles Repository"
    
    if [[ -d "$HOME/.local/share/chezmoi" ]]; then
        log_warning "chezmoi directory already exists, updating..."
        cd "$HOME/.local/share/chezmoi"
        git pull
    else
        log_info "Initializing chezmoi with dotfiles repository..."
        chezmoi init "$DOTFILES_REPO"
    fi
    
    log_info "Applying dotfiles configuration..."
    chezmoi apply
    
    log_success "Dotfiles configuration applied"
}

# Install all Homebrew packages
install_packages() {
    log_section "Installing All System Packages"
    
    if [[ -f "$HOME/.Brewfile" ]]; then
        log_info "Installing packages from Brewfile..."
        cd "$HOME"
        brew bundle --no-lock
        log_success "All packages installed successfully"
    else
        log_error "Brewfile not found at $HOME/.Brewfile"
        exit 1
    fi
}

# Configure shell environment
setup_shell() {
    log_section "Configuring Shell Environment"
    
    # Check if zsh is the default shell
    if [[ "$SHELL" != "/bin/zsh" && "$SHELL" != "/opt/homebrew/bin/zsh" ]]; then
        log_info "Setting zsh as default shell..."
        sudo chsh -s /bin/zsh "$USER"
        log_warning "Shell changed to zsh. Please restart your terminal after setup completes."
    fi
    
    # Source the configuration to ensure everything is loaded
    if [[ -f "$HOME/.zshrc" ]]; then
        log_info "zsh configuration is ready"
        log_success "Shell environment configured"
    else
        log_error "zsh configuration not found"
        exit 1
    fi
}

# Setup Claude Code integration
setup_claude_code() {
    log_section "Configuring Claude Code Integration"
    
    if [[ -d "$HOME/.claude" ]]; then
        log_info "Claude Code configuration directory found"
        
        # Verify key components exist
        local components=(
            "$HOME/.claude/agents"
            "$HOME/.claude/memories"
            "$HOME/.claude/hooks"
            "$HOME/.claude/settings.json"
        )
        
        for component in "${components[@]}"; do
            if [[ -e "$component" ]]; then
                log_success "✓ $(basename "$component") configured"
            else
                log_error "✗ $(basename "$component") missing"
            fi
        done
        
        log_success "Claude Code integration ready"
    else
        log_warning "Claude Code configuration not found - will be available after first Claude Code run"
    fi
}

# Verify installation
verify_installation() {
    log_section "Verifying Installation"
    
    local tools=(
        "brew"
        "chezmoi" 
        "git"
        "zsh"
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
    
    log_info "Checking essential tools..."
    local missing=0
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            log_success "✓ $tool available"
        else
            log_error "✗ $tool not found"
            ((missing++))
        fi
    done
    
    if [[ $missing -eq 0 ]]; then
        log_success "All essential tools installed successfully!"
    else
        log_error "$missing tools are missing. Please check the installation."
        exit 1
    fi
}

# Final setup instructions
show_completion() {
    log_section "Setup Complete! 🎉"
    
    echo
    echo -e "${GREEN}Your terminal-first development environment is ready!${NC}"
    echo
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Restart your terminal to load the new shell configuration"
    echo "2. Run 'yazi' to explore the modern file manager"
    echo "3. Run 'helix' to try the modern modal editor"
    echo "4. Check out the documentation at: https://nehalecky.github.io/dotfiles/"
    echo
    echo -e "${PURPLE}Key commands to remember:${NC}"
    echo "• 'workspace-home' - Launch the home command center"
    echo "• 'workspace-dev' - Launch the development workspace"
    echo "• 'task list' - View your current tasks"
    echo "• 'glow ~/.docs/README.md' - Browse documentation locally"
    echo
    echo -e "${YELLOW}Pro tip:${NC} The system uses Ctrl+a as the leader key for terminal operations"
    echo
    log_success "Welcome to your new development environment!"
}

# Main execution flow
main() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║        macOS Development Environment Bootstrap Script        ║"
    echo "║                  by Nicholaus Eugene Halecky                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    
    log_info "Starting macOS development environment setup..."
    echo
    
    check_system
    install_homebrew
    install_chezmoi
    setup_dotfiles
    install_packages
    setup_shell
    setup_claude_code
    verify_installation
    show_completion
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi