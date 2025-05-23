#!/usr/bin/env sh
# XDG Base Directory Specification compliance
# This file sets environment variables to move configs out of $HOME

# XDG Base Directories
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Development Tools
export CONDARC="$XDG_CONFIG_HOME/conda/condarc"
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"

# Python
export JUPYTER_CONFIG_DIR="$XDG_CONFIG_HOME/jupyter"
export IPYTHONDIR="$XDG_CONFIG_HOME/ipython"
export PYLINTHOME="$XDG_CACHE_HOME/pylint"
export PYTHONSTARTUP="$XDG_CONFIG_HOME/python/pythonrc"
export WORKON_HOME="$XDG_DATA_HOME/virtualenvs"

# Security
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
export GOPASS_CONFIG="$XDG_CONFIG_HOME/gopass"
export GOPASS_HOMEDIR="$XDG_DATA_HOME/gopass"

# Shell/CLI Tools
export ZDOTDIR="$HOME"  # Keep zsh configs in home for now
export HISTFILE="$XDG_STATE_HOME/zsh/history"
export LESSHISTFILE="$XDG_CACHE_HOME/less/history"
export NODE_REPL_HISTORY="$XDG_DATA_HOME/node_repl_history"

# Application Data
export JULIA_DEPOT_PATH="$XDG_DATA_HOME/julia:$JULIA_DEPOT_PATH"
export BUNDLE_USER_CONFIG="$XDG_CONFIG_HOME/bundle"
export BUNDLE_USER_CACHE="$XDG_CACHE_HOME/bundle"
export BUNDLE_USER_PLUGIN="$XDG_DATA_HOME/bundle"
export GEM_HOME="$XDG_DATA_HOME/gem"
export GEM_SPEC_CACHE="$XDG_CACHE_HOME/gem"

# Cache directories
export PIP_CACHE_DIR="$XDG_CACHE_HOME/pip"
export YARN_CACHE_FOLDER="$XDG_CACHE_HOME/yarn"

# Create required directories
for dir in \
    "$XDG_CONFIG_HOME" \
    "$XDG_CACHE_HOME" \
    "$XDG_DATA_HOME" \
    "$XDG_STATE_HOME" \
    "$XDG_STATE_HOME/zsh" \
    "$XDG_CACHE_HOME/less"
do
    [ ! -d "$dir" ] && mkdir -p "$dir"
done