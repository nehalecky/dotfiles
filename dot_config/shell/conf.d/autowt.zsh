# autowt — automatic worktree shell integration
# Adds ~/bin to PATH (where autowt/awt binaries live) and initialises the
# shell functions that let autowt switch the *current* shell's directory
# rather than opening a new terminal tab.
export PATH="$HOME/bin:$PATH"
command -v autowt &>/dev/null && eval "$(autowt shell-init zsh)"
