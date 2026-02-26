# Secrets Management Guide

This guide explains the secrets management strategy using chezmoi with 1Password as the single source of truth.

## Overview

All secrets are managed through **1Password**. There is no encrypted-file fallback. The approach is:

1. **1Password** - Single canonical source for all secrets
2. **Dynamic Resolution** - Templates pull from 1Password at `chezmoi apply` time
3. **Profile-Aware Keys** - SSH key names are configurable per profile (personal vs. work)

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

At `chezmoi init` time, you are prompted for profile identity and key names. These are stored in `~/.config/chezmoi/chezmoi.toml` (local machine config, never committed to the repository).

### Prompted Variables

| Variable | Purpose | Personal Default |
|---|---|---|
| `op_auth_key_name` | 1Password item name for your SSH authentication key | "GitHub SSH Auth Key" |
| `op_signing_key_name` | 1Password item name for your SSH signing key | "Git Commit Signing Key" |

Work profiles have no defaults — you must specify the vault item names that match your work 1Password setup.

### How They Are Used

These variables are rendered into `~/.config/1Password/ssh/agent.toml` via the chezmoi template at `dot_config/1Password/ssh/agent.toml.tmpl`:

```toml
# Rendered from dot_config/1Password/ssh/agent.toml.tmpl
[[ssh-keys]]
item = "GitHub SSH Auth Key"   # ← from op_auth_key_name

[[ssh-keys]]
item = "Git Commit Signing Key"  # ← from op_signing_key_name
```

The template source:
```toml
[[ssh-keys]]
item = {{ .op_auth_key_name | quote }}

[[ssh-keys]]
item = {{ .op_signing_key_name | quote }}
```

## SSH Commit Signing

This setup uses SSH commit signing with 1Password instead of GPG for verified commits.

### Configuration

The git configuration is managed as a chezmoi template at `dot_config/git/config.tmpl`. The signing key is injected at `chezmoi init` time from the `git_signing_key` prompt and stored in `~/.config/chezmoi/chezmoi.toml`.

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

After rendering, `~/.config/git/config` contains the actual public key value from your `git_signing_key` prompt — for example:

```gitconfig
[user]
    signingkey = ssh-ed25519 AAAAC3NzaC1lZDI1NTE5...  # your actual key after rendering
```

### Benefits
- **Unified Key Management**: Same 1Password vault manages SSH auth and signing keys
- **Profile Portability**: Different machines or profiles specify their own 1Password item names at init time
- **Simpler Setup**: No GPG key generation, distribution, or expiration management
- **Consistent Workflow**: Leverages existing SSH infrastructure
- **GitHub Native Support**: Full verification support since 2022

### Usage
Once configured, all commits are automatically signed. The SSH public key must be added to GitHub as a "Signing Key" (separate from authentication keys).

## Implementation Guide

### 1. Store Secret in 1Password (Canonical Source)

```bash
# Create an entry in 1Password
op item create \
  --category=api_credential \
  --title="MyApp API Key" \
  --vault="Personal" \
  api_key="sk-xxxxxxxxxxxx"
```

### 2. Reference Secret in a Chezmoi Template

File: `~/.config/myapp/config.yml.tmpl`
```yaml
# Template that pulls from 1Password at apply time
api:
  key: {{ onepasswordRead "op://Personal/MyApp API Key/api_key" }}
```

### 3. Add to Chezmoi

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

Use chezmoi data variables (set in `chezmoi.toml`) to branch on profile:

```yaml
{{- if .isWork }}
key: {{ onepasswordRead "op://Work/api/key" }}
{{- else }}
key: {{ onepasswordRead "op://Personal/api/key" }}
{{- end }}
```

## Best Practices

1. **1Password is the only source of truth**
   - Never hardcode secrets in templates or committed files
   - Never store secrets in `.chezmoidata.yaml` (committed to repo)

2. **Profile identity lives in `~/.config/chezmoi/chezmoi.toml`**
   - This file is local to the machine and never committed
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

- **No encrypted fallback files** - 1Password is required; there is no offline secret storage in this repo
- **Local config only** - `~/.config/chezmoi/chezmoi.toml` holds identity data and is never committed
- **Git Storage** - No secrets or encrypted blobs are stored in the repository
- **Rotation** - Update the secret in 1Password; run `chezmoi apply` to pick up the new value

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

If you need to update the key names (e.g., switching from personal to work setup), edit `~/.config/chezmoi/chezmoi.toml` directly:

```toml
[data]
  op_auth_key_name = "Work GitHub Auth Key"
  op_signing_key_name = "Work Git Signing Key"
```

Then run `chezmoi apply` to re-render the affected templates.

## References

- [Chezmoi Password Managers](https://www.chezmoi.io/user-guide/password-managers/)
- [Chezmoi 1Password Integration](https://www.chezmoi.io/user-guide/password-managers/1password/)
- [1Password CLI](https://developer.1password.com/docs/cli/)
- [GitHub SSH Commit Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification#ssh-commit-signature-verification)
