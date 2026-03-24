# Secrets Management Guide

This guide covers secrets management with chezmoi and 1Password as the single source of truth.

## Overview

**1Password** manages all secrets. There is no encrypted-file fallback.

1. **1Password** - Single canonical source for all secrets
2. **Dynamic Resolution** - Templates pull secrets from 1Password at `chezmoi apply` time
3. **Profile-Aware Keys** - SSH key names vary per profile (personal vs. work)

## Architecture

```
┌─────────────┐
│  1Password  │ ← Single source of truth
└──────┬──────┘
       │
       ├─── chezmoi templates (dot_config/git/config.tmpl, etc.)
       │    └─→ op-ssh-sign / 1Password CLI injects secrets at apply time
       │
       └─── ~/.config/chezmoi/chezmoi.toml (local, never committed)
            └─→ Stores profile identity and 1Password item names
```

## Profile-Aware 1Password Key Names

At `chezmoi init` time, chezmoi prompts for profile identity and key names. It stores them in `~/.config/chezmoi/chezmoi.toml` (local machine config, never committed).

### Prompted Variables

| Variable | Purpose | Note |
|---|---|---|
| `op_auth_key_name` | 1Password item name for your SSH authentication key | Must match your vault exactly — no default |
| `op_signing_key_name` | 1Password item name for your SSH signing key | Must match your vault exactly — no default |

> **Critical:** These names are case-sensitive and must match the item title in your 1Password vault character-for-character. Open 1Password, filter by SSH Key category, and copy the title. See `examples/chezmoi.toml.example` for guidance.

Work profiles have no defaults — specify the vault item names that match your work 1Password setup.

### How Chezmoi Uses Them

Chezmoi renders these variables into `~/.config/1Password/ssh/agent.toml` via `dot_config/1Password/ssh/agent.toml.tmpl`:

```toml
# Rendered from dot_config/1Password/ssh/agent.toml.tmpl
# (example — actual item names come from your chezmoi.toml)
[[ssh-keys]]
item = "Nico Personal GitHub Auth Key"   # ← from op_auth_key_name

[[ssh-keys]]
item = "Github Signing Key (Nico Personal)"  # ← from op_signing_key_name
```

The template source:
```toml
[[ssh-keys]]
item = {{ .op_auth_key_name | quote }}

[[ssh-keys]]
item = {{ .op_signing_key_name | quote }}
```

## SSH Commit Signing

This setup signs commits with SSH keys via 1Password instead of GPG.

### Configuration

Chezmoi manages the git configuration as a template at `dot_config/git/config.tmpl`. At `chezmoi init` time, the `git_signing_key` prompt injects the signing key into `~/.config/chezmoi/chezmoi.toml`.

The template:
```gitconfig
# Rendered from dot_config/git/config.tmpl
[user]
    name = {{ .git_name }}
    email = {{ .git_email }}

[commit]
    gpgsign = true

[gpg]
    format = ssh

[gpg "ssh"]
    allowedSignersFile = {{ .chezmoi.homeDir }}/.ssh/allowed_signers
    program = "/Applications/1Password.app/Contents/MacOS/op-ssh-sign"

{{- if .git_signing_key }}
[user]
    signingkey = {{ .git_signing_key }}
{{- end }}
```

After rendering, `~/.config/git/config` contains the actual public key from `git_signing_key`:

```gitconfig
[user]
    signingkey = ssh-ed25519 AAAAC3NzaC1lZDI1NTE5...  # your actual key after rendering
```

### Benefits
- **Unified Key Management**: One 1Password vault manages both SSH auth and signing keys
- **Profile Portability**: Each machine or profile specifies its own 1Password item names at init time
- **Simpler Setup**: No GPG key generation, distribution, or expiration management
- **Consistent Workflow**: Builds on existing SSH infrastructure
- **GitHub Native Support**: Full verification support since 2022

### Usage
Once configured, git signs all commits automatically. Add the SSH public key to GitHub as a "Signing Key" (separate from authentication keys).

## Implementation Guide

### 1. Store the Secret in 1Password

```bash
# Create an entry in 1Password
op item create \
  --category=api_credential \
  --title="MyApp API Key" \
  --vault="Personal" \
  api_key="sk-xxxxxxxxxxxx"
```

### 2. Reference the Secret in a Chezmoi Template

File: `~/.config/myapp/config.yml.tmpl`
```yaml
# Template that pulls from 1Password at apply time
api:
  key: {{ onepasswordRead "op://Personal/MyApp API Key/api_key" }}
```

### 3. Add the Template to Chezmoi

```bash
# Add the template file (from HOME directory)
chezmoi add ~/.config/myapp/config.yml

# Verify the template renders correctly
chezmoi execute-template < ~/.local/share/chezmoi/dot_config/myapp/config.yml.tmpl

# Commit the template
chezmoi git -- commit -m "feat: add myapp configuration template"
```

## Managing Different Secret Types

### Simple Values (API Keys, Tokens)

```yaml
token: {{ onepasswordRead "op://Vault/Item/field" }}
```

### Documents (SSL Certificates, SSH Keys)

```yaml
{{- onepasswordDocument "item-uuid" | b64dec -}}
```

### Environment-Specific Secrets

Branch on profile using chezmoi data variables (set in `chezmoi.toml`):

```yaml
{{- if .isWork }}
key: {{ onepasswordRead "op://Work/api/key" }}
{{- else }}
key: {{ onepasswordRead "op://Personal/api/key" }}
{{- end }}
```

## Best Practices

1. **Keep 1Password as the only source of truth**
   - Never hardcode secrets in templates or committed files
   - Never store secrets in `.chezmoidata.yaml` (committed to repo)

2. **Store profile identity in `~/.config/chezmoi/chezmoi.toml`**
   - This file stays local to the machine and is never committed
   - Contains `op_auth_key_name`, `op_signing_key_name`, `git_signing_key`, etc.

3. **Document secret requirements**
   - List all required 1Password entries in setup guides
   - Include vault name and item name so other machines can reproduce

4. **Test template rendering**
   ```bash
   # Preview rendered output without applying
   chezmoi execute-template < ~/.local/share/chezmoi/dot_config/git/config.tmpl

   # Full dry run
   chezmoi apply --dry-run
   ```

## Security Considerations

- **No encrypted fallback files** - 1Password is required; the repo contains no offline secret storage
- **Local config only** - `~/.config/chezmoi/chezmoi.toml` holds identity data and is never committed
- **No secrets in Git** - The repository stores no secrets or encrypted blobs
- **Rotation** - Update the secret in 1Password, then run `chezmoi apply` to propagate the new value

## API Keys and TTS Backends

Claude Code hooks use a priority chain for voice notifications:
**ElevenLabs → OpenAI TTS → Kokoro (local) → pyttsx3**

### Kokoro (default — no API key required)

Kokoro is the default TTS backend when no cloud keys are set. It runs the `kokoro-82M v1.0` OSS neural model locally via `uv run`, downloading ~90 MB from Hugging Face on first use.

Pre-warm before your first session:
```bash
uv run ~/.claude/hooks/utils/tts/kokoro_tts.py "Kokoro ready"
```

Voice is set via `KOKORO_VOICE` in `~/.env` (see below). Default: `af_heart` (warm American female).

### Cloud TTS backends (optional, higher quality)

Store API keys in 1Password and reference them in `~/.env` via chezmoi template:

```bash
# In ~/.local/share/chezmoi/private_dot_env.tmpl:
export ELEVENLABS_API_KEY='{{ onepasswordRead "op://Personal/ElevenLabs/api_key" }}'
export OPENAI_API_KEY='{{ onepasswordRead "op://Personal/OpenAI/api_key" }}'
```

Run `chezmoi apply` after editing the template to render the keys to `~/.env`.

### `~/.env` and chezmoi

`~/.env` is managed by `private_dot_env.tmpl`. It is:
- **Rendered** at `chezmoi apply` time — 1Password values are injected then
- **Never committed** — `private_` prefix means chezmoi encrypts before storing (actually this file is excluded from the public repo)
- **Sourced** by your shell at login

To add a new secret:
1. Store the value in 1Password
2. Add a line to `private_dot_env.tmpl` using `{{ onepasswordRead "op://Vault/Item/field" }}`
3. Run `chezmoi apply`

## Troubleshooting

### Secret not found in 1Password

```bash
# List available items
op item list --vault Personal

# Check exact URI
op read "op://Vault/Item/field" --reveal
```

### Template syntax errors

```bash
# Test template rendering
chezmoi execute-template < template.tmpl
```

### SSH agent not offering the right keys

```bash
# Check what the rendered agent.toml looks like
chezmoi cat ~/.config/1Password/ssh/agent.toml

# Verify the item names match what is in 1Password
op item get "GitHub SSH Auth Key" --vault Personal
```

### Wrong key name after profile switch

To update key names (e.g., when switching from personal to work), edit `~/.config/chezmoi/chezmoi.toml` directly:

```toml
[data]
  op_auth_key_name = "Work GitHub Auth Key"
  op_signing_key_name = "Work Git Signing Key"
```

Then run `chezmoi apply` to re-render affected templates.

## References

- [Chezmoi Password Managers](https://www.chezmoi.io/user-guide/password-managers/)
- [Chezmoi 1Password Integration](https://www.chezmoi.io/user-guide/password-managers/1password/)
- [1Password CLI](https://developer.1password.com/docs/cli/)
- [GitHub SSH Commit Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification#ssh-commit-signature-verification)
