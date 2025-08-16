#!/bin/bash

# Claude Code Status Line - Inspired by Starship configuration
# Captures key elements: directory, git status, and time

input=$(cat)
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')
model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')

# Get current directory basename for display
dir_name=$(basename "$current_dir")
if [[ "$current_dir" == "$HOME" ]]; then
    dir_name="~"
elif [[ "$current_dir" == "/" ]]; then
    dir_name="/"
fi

# Get git branch if in a git repository
git_info=""
if git -C "$current_dir" rev-parse --git-dir >/dev/null 2>&1; then
    branch=$(git -C "$current_dir" branch --show-current 2>/dev/null)
    if [[ -n "$branch" ]]; then
        # Check for git status
        if ! git -C "$current_dir" diff-index --quiet HEAD -- 2>/dev/null; then
            git_info=" $branch*"
        else
            git_info=" $branch"
        fi
    fi
fi

# Get current time
current_time=$(date +"%H:%M")

# Build status line with colors (using printf for ANSI codes)
printf "\033[2m\033[36m%s\033[0m \033[2m\033[94m%s\033[0m%s \033[2m\033[33m%s\033[0m" \
    "$model_name" \
    "$dir_name" \
    "$git_info" \
    "$current_time"