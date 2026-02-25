# Setup Guide

Detailed onboarding for new machines and profile changes.

## Quick Start

### New machine setup

1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install chezmoi and initialize:
   ```bash
   brew install chezmoi
   chezmoi init --apply nehalecky
   ```

3. Answer the setup prompts:
   - **Machine profile**: `personal` or `work`
   - **Git author name**: Your full name
   - **Preferred/casual name**: What you like to be called (defaults to first word of full name)
   - **Git email**: Your email for commits
   - **GitHub username**: Your GitHub handle
   - **Git signing public key**: Your SSH public key (`ssh-ed25519 ...`)
   - **1Password SSH auth key name**: Item name in 1Password for your auth key
   - **1Password signing key name**: Item name in 1Password for your signing key

4. Run brew bundle to install packages:
   ```bash
   brew bundle --global
   ```

### Re-initializing (change profile or update values)

To change any prompted value, delete it from `~/.config/chezmoi/chezmoi.toml` and re-run:

```bash
chezmoi init --apply nehalecky
```

Or edit the value directly in `~/.config/chezmoi/chezmoi.toml` and run `chezmoi apply`.

## What the profiles control

| Setting | `personal` | `work` |
|---------|-----------|--------|
| Git identity | personal email + key | work email + key |
| Brewfile | personal apps (Signal, Spotify, Steam) | work tools (k9s, kubectl, Docker, Slack) |
| Starship prompt | minimal, clean | shows Kubernetes context, hostname |
| SSH allowed_signers | personal key | work key |
| 1Password agent | personal vault keys | work vault keys |
| `.ssh/id_ed25519_signing.pub` | deployed | excluded |
| `.kube/`, `.aws/` | excluded | excluded (managed by cloud CLIs) |

## Day 1 work machine setup (after chezmoi apply)

After running `chezmoi init --apply` with the `work` profile:

1. Authenticate GitHub CLI:
   ```bash
   gh auth login
   ```

2. Set up GCP credentials:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. Authenticate 1Password CLI:
   ```bash
   op signin
   ```

## Troubleshooting

### Config template changed warning

If you see `chezmoi: warning: config file template has changed, run chezmoi init to regenerate config file`, your local `~/.config/chezmoi/chezmoi.toml` is missing a newly added variable. Either:

- Run `chezmoi init --apply nehalecky` to regenerate (you will be prompted for new values)
- Or add the missing key manually to `~/.config/chezmoi/chezmoi.toml` under `[data]`

### 1Password SSH signing errors

If commits fail with `1Password: agent returned an error`, ensure:

1. 1Password desktop app is running and unlocked
2. The SSH agent is enabled in 1Password Settings > Developer > SSH Agent
3. The correct key names are set in `~/.config/chezmoi/chezmoi.toml` (`op_auth_key_name`, `op_signing_key_name`)

### Checking what chezmoi will change

```bash
chezmoi diff          # Preview all pending changes
chezmoi apply --dry-run  # Dry-run without writing
chezmoi verify        # Validate all managed files
```
