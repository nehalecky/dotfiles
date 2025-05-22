# dotfiles

Modern dotfiles management with [chezmoi](https://chezmoi.io/).

## Setup

1. **Install chezmoi** (already installed):
   ```bash
   brew install chezmoi
   ```

2. **Initialize from this repository**:
   ```bash
   chezmoi init nehalecky/dotfiles
   ```

3. **Apply the configuration**:
   ```bash
   chezmoi apply
   ```

## What's Managed

- **SSH Configuration**: 1Password agent integration with proper key selection
- **Git Configuration**: Signing keys and user settings
- **Zsh Environment**: Complete prezto setup with Powerlevel10k prompt
- **1Password**: SSH agent configuration for dynamic key selection

## Key Features

- **Secure**: Private keys stored in 1Password, public keys in repo
- **Dynamic**: SSH keys resolved at runtime from 1Password agent
- **Clean**: Real configuration content, not symlink paths
- **Portable**: Easy setup on new machines

## Migration Notes

This setup replaces a previous bare git repository approach and resolves symlink management issues by capturing actual file content using `chezmoi add --follow`.