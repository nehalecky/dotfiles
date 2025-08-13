# Claude Code Trust Configuration

## Auto-Trust Home Directory

To avoid the trust dialog when launching Claude Code in your home directory:

**Manual Configuration:**
Edit `~/.claude.json` and set:
```json
{
  "projects": {
    "/Users/nehalecky": {
      "hasTrustDialogAccepted": true
    }
  }
}
```

**Status:** ✅ Configured (2025-01-13)

## Security Note

The `.claude.json` file contains sensitive MCP server tokens:
- GitHub Personal Access Token (`ghp_...`)
- Hugging Face Access Token (`hf_...`)

**Do NOT version control** this file due to security tokens. Only the trust settings are safe to replicate.

## PATH Warning

Claude Code may show a PATH warning even when `~/.local/bin` is correctly configured. This is a detection issue - the commands work properly despite the warning.

**Current PATH Status:** ✅ Working
- `/Users/nehalecky/.local/bin` is in PATH
- Commands like `workspace-home`, `weather-display` execute correctly