# Secrets Management Guide

This guide explains the hybrid secrets management strategy using chezmoi with 1Password as the canonical source.

## Overview

We use a **hybrid approach with 1Password as the single source of truth**:
1. **1Password** - Canonical source for all secrets
2. **Dynamic Resolution** - Pull from 1Password when available
3. **Encrypted Fallback** - Age-encrypted files for restricted environments
4. **Automatic Detection** - Smart switching based on environment

## Architecture

```
┌─────────────┐
│  1Password  │ ← Single source of truth
└──────┬──────┘
       │
       ├─── Development Environment (1Password available)
       │    └─→ Templates pull directly from 1Password
       │
       └─── Restricted Environment (No 1Password)
            └─→ Use pre-encrypted files (synced from 1Password)
```

## Environment Detection Strategy

Chezmoi automatically detects the environment and chooses the appropriate method:

```go
{{- $has1Password := lookPath "op" -}}
{{- if $has1Password -}}
  # Use 1Password directly
  api_key: {{ onepasswordRead "op://Personal/myapp/api_key" }}
{{- else -}}
  # Fall back to encrypted file
  {{- include ".secrets/myapp-api-key.age" | decrypt -}}
{{- end -}}
```

## Implementation Guide

### 1. Store Secret in 1Password (Canonical Source)

```bash
# Create entry in 1Password
op item create \
  --category=api_credential \
  --title="MyApp API Key" \
  --vault="Personal" \
  api_key="sk-xxxxxxxxxxxx"
```

### 2. Create Hybrid Template

File: `~/.config/myapp/config.yml.tmpl`
```yaml
# Hybrid template that works in both environments
api:
  {{- if lookPath "op" }}
  # 1Password is available - pull directly
  key: {{ onepasswordRead "op://Personal/MyApp API Key/api_key" }}
  {{- else }}
  # No 1Password - use encrypted fallback
  key: {{ include ".secrets/myapp-api-key.age" | decrypt }}
  {{- end }}
```

### 3. Sync Secret to Encrypted File

Create a sync script to pull from 1Password and encrypt:

```bash
#!/bin/bash
# scripts/sync-secrets.sh
# Pulls secrets from 1Password and creates encrypted files

# Ensure we're signed in
eval $(op signin)

# Pull secret from 1Password
SECRET=$(op read "op://Personal/MyApp API Key/api_key")

# Encrypt and save
echo -n "$SECRET" | chezmoi age encrypt > .local/share/chezmoi/.secrets/myapp-api-key.age

echo "✓ Synced MyApp API key"
```

### 4. Add to Chezmoi

```bash
# Add the template
chezmoi add ~/.config/myapp/config.yml.tmpl

# Add the encrypted secret (for fallback)
chezmoi add .secrets/myapp-api-key.age
```

## Workflow Examples

### Development Machine (with 1Password)

1. Templates resolve directly from 1Password
2. No encrypted files needed locally
3. Always gets latest secret values

### Server/CI Environment (without 1Password)

1. Templates detect missing `op` command
2. Falls back to encrypted files
3. Secrets remain secure with age encryption

## Managing Different Secret Types

### Simple Values (API Keys, Tokens)

```yaml
# Template with fallback
token: {{- if lookPath "op" -}}
  {{ onepasswordRead "op://Vault/Item/field" }}
{{- else -}}
  {{ include ".secrets/token.age" | decrypt }}
{{- end -}}
```

### Complex Files (SSL Certificates, SSH Keys)

```yaml
# For larger files, always use encryption
{{- if lookPath "op" -}}
  {{- onepasswordDocument "uuid" | b64dec -}}
{{- else -}}
  {{- include ".secrets/certificate.age" | decrypt -}}
{{- end -}}
```

### Environment-Specific Secrets

```yaml
# Use chezmoi's data to determine environment
{{- $env := .chezmoi.hostname -}}
{{- if eq $env "production" -}}
  {{- if lookPath "op" -}}
    key: {{ onepasswordRead "op://Production/api/key" }}
  {{- else -}}
    key: {{ include ".secrets/prod-api-key.age" | decrypt }}
  {{- end -}}
{{- end -}}
```

## Automation Scripts

### Sync All Secrets

Create `.local/share/chezmoi/scripts/sync-all-secrets.sh`:

```bash
#!/bin/bash
# Sync all secrets from 1Password to encrypted files

set -e

echo "Syncing secrets from 1Password..."

# Ensure signed in
eval $(op signin) || exit 1

# Define secrets to sync
declare -A SECRETS=(
  ["github-token"]="op://Personal/GitHub/token"
  ["aws-key"]="op://Work/AWS/access_key"
  ["aws-secret"]="op://Work/AWS/secret_key"
)

# Sync each secret
for name in "${!SECRETS[@]}"; do
  uri="${SECRETS[$name]}"
  echo -n "Syncing $name... "
  
  # Pull from 1Password and encrypt
  op read "$uri" | chezmoi age encrypt > ".secrets/${name}.age"
  
  echo "✓"
done

echo "All secrets synced!"
```

### Verify Secrets

```bash
#!/bin/bash
# Verify encrypted secrets match 1Password

for file in .secrets/*.age; do
  name=$(basename "$file" .age)
  decrypted=$(chezmoi age decrypt < "$file")
  # Compare with 1Password (implementation depends on secret structure)
done
```

## Best Practices

1. **Always use 1Password as source of truth**
   - Never edit encrypted files directly
   - Run sync script after updating 1Password

2. **Version control encrypted files**
   - Safe to commit `.age` files to git
   - They're encrypted with your age key

3. **Document secret requirements**
   - List all required 1Password entries
   - Include vault and item names

4. **Test both paths**
   ```bash
   # Test with 1Password
   chezmoi apply --dry-run
   
   # Test without (temporarily rename op)
   sudo mv /opt/homebrew/bin/op /opt/homebrew/bin/op.bak
   chezmoi apply --dry-run
   sudo mv /opt/homebrew/bin/op.bak /opt/homebrew/bin/op
   ```

5. **Regular sync**
   - Run sync script in CI/CD
   - Or before deploying to new environments

## Security Considerations

- **1Password Access**: Development machines only
- **Age Encryption**: Uses your personal age key
- **Git Storage**: Encrypted files are safe to commit
- **Rotation**: Update in 1Password, then sync

## Troubleshooting

### Secret not found in 1Password
```bash
# List available items
op item list --vault Personal

# Check exact URI
op read "op://Vault/Item/field" --reveal
```

### Decryption fails
```bash
# Check age key
chezmoi age decrypt --help

# Verify encryption
cat .secrets/file.age | chezmoi age decrypt
```

### Template syntax errors
```bash
# Test template rendering
chezmoi execute-template < template.tmpl
```

## SSH Commit Signing

This setup uses SSH commit signing with 1Password instead of GPG for verified commits.

### Configuration
The git configuration uses SSH signing with the 1Password SSH agent:

```toml
[commit]
    gpgsign = true

[gpg]
    format = ssh

[gpg "ssh"]
    program = "/Applications/1Password.app/Contents/MacOS/op-ssh-sign"

[user]
    signingkey = ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGfxtbZHZuHkiMv2ZXR52KSwROrTXK0wyxoX8yd88Ih6
```

### Benefits
- **Unified Key Management**: Same 1Password vault manages SSH auth and signing keys
- **Simpler Setup**: No GPG key generation, distribution, or expiration management
- **Consistent Workflow**: Leverages existing SSH infrastructure
- **GitHub Native Support**: Full verification support since 2022

### Usage
Once configured, all commits are automatically signed. The SSH public key must be added to GitHub as a "Signing Key" (separate from authentication keys).

## References

- [Chezmoi Password Managers](https://www.chezmoi.io/user-guide/password-managers/)
- [Chezmoi 1Password Integration](https://www.chezmoi.io/user-guide/password-managers/1password/)
- [Chezmoi Encryption](https://www.chezmoi.io/user-guide/encryption/)
- [1Password CLI](https://developer.1password.com/docs/cli/)
- [GitHub SSH Commit Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification#ssh-commit-signature-verification)