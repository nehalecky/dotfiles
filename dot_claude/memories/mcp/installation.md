# MCP Server Installation and Management

## Installation Philosophy
**MCP integration should be straightforward and well-researched. Always start with understanding what's available before attempting installation.**

## Required Installation Process

### 1. General Search First
**CRITICAL:** Always start with comprehensive research before attempting installation.

```bash
# Research what MCP servers are available for a service
# Search "[service] MCP server" to understand options
# Examples:
# - "GitHub MCP server" 
# - "Hugging Face MCP server"
# - "Slack MCP server"
```

**Research Questions:**
- What official MCP servers exist for this service?
- What authentication methods are supported?
- Are there community-maintained alternatives?
- What transport protocols are available (http, stdio, sse)?

### 2. Find Official Documentation
Look for official installation instructions and configuration details:

- Check `service.com/settings/mcp` or similar configuration pages
- Review official GitHub repositories for MCP servers
- Look for authentication token requirements
- Understand rate limits and usage constraints

### 3. Use Standard Tooling
Apply `claude mcp add` command with appropriate parameters:

```bash
# Basic syntax
claude mcp add [server-name] [server-path] [options]

# Common patterns
claude mcp add github github.com/github/github-mcp-server
claude mcp add server-name -t http "https://api.service.com/mcp"
claude mcp add server-name -t stdio /path/to/executable
```

#### Transport Types
- **`stdio`** - Direct executable communication
- **`http`** - HTTP-based API communication  
- **`sse`** - Server-sent events for real-time updates

#### Authentication Patterns
```bash
# Bearer token with 1Password integration
claude mcp add service -t http "https://api.service.com/mcp" \
  -H "Authorization:Bearer $(op read 'op://Private/service-token/credential')"

# API key authentication
claude mcp add service -t http "https://api.service.com/mcp" \
  -H "X-API-Key:$(op read 'op://Private/service-api-key/password')"

# Multiple headers
claude mcp add service -t http "https://api.service.com/mcp" \
  -H "Authorization:Bearer $(op read 'op://Private/token/credential')" \
  -H "User-Agent:claude-code-client"
```

### 4. Validate Properly
**Only claim success when verification confirms proper connection:**

```bash
# Verify installation success
claude mcp list

# Expected output shows "✓ Connected" status
# Example:
# github: ✓ Connected (github.com/github/github-mcp-server)
# hf-mcp-server: ✓ Connected (https://huggingface.co/mcp)
```

## Installation Verification

### Connection Testing
```bash
# Test basic connectivity
claude mcp list                          # Show all configured servers
claude mcp test [server-name]            # Test specific server connection
claude mcp status                        # Detailed connection status

# Debug connection issues
CLAUDE_LOG=debug claude mcp list         # Verbose logging
CLAUDE_LOG=debug claude mcp test github  # Debug specific server
```

### Common Connection States
- **✓ Connected** - Server is accessible and responding
- **⚠ Warning** - Connected but with issues (rate limits, partial access)
- **✗ Failed** - Cannot connect (auth issues, network problems)
- **⏳ Connecting** - Initial connection in progress

## Error Resolution

### Authentication Issues
```bash
# Token expiration
# Re-read token from 1Password and reinstall
claude mcp remove server-name
claude mcp add server-name -t http "url" -H "Authorization:Bearer $(op read 'op://vault/item/field')"

# Invalid token format
# Verify token format requirements in service documentation
# Some services require "Bearer ", others just the token
```

### Network and Transport Issues
```bash
# HTTP transport issues
# Verify URL accessibility
curl -I "https://api.service.com/mcp"

# Stdio transport issues  
# Verify executable exists and is executable
which mcp-server-executable
chmod +x /path/to/mcp-server

# Check logs for detailed error information
tail -f ~/.claude/logs/mcp.log
```

### Version Compatibility
```bash
# Update Claude Code to latest version
brew upgrade claude

# Check MCP server version compatibility
claude mcp info [server-name]           # Show server version info
claude --version                        # Show Claude version

# Reinstall server if version mismatch
claude mcp remove [server-name]
claude mcp add [server-name] [latest-config]
```

## Management Operations

### Server Lifecycle
```bash
# List all servers
claude mcp list                         # Basic list
claude mcp list --verbose              # Detailed information

# Remove servers
claude mcp remove [server-name]        # Remove specific server
claude mcp remove --all                # Remove all servers (dangerous)

# Update server configuration
claude mcp remove [server-name]
claude mcp add [server-name] [new-config]

# Disable/enable without removing
claude mcp disable [server-name]       # Temporarily disable
claude mcp enable [server-name]        # Re-enable disabled server
```

### Configuration Management
```bash
# Export configuration for backup
claude mcp export > mcp-config.json

# Import configuration (restore)
claude mcp import < mcp-config.json

# Show configuration file location
claude config show mcp
```

## Best Practices

### Security Considerations
- **Use 1Password for tokens** - Never store credentials in plain text
- **Rotate tokens regularly** - Set up token rotation schedules
- **Principle of least privilege** - Use tokens with minimal required permissions
- **Monitor access logs** - Check service logs for unexpected usage

### Performance Optimization
- **Monitor rate limits** - Respect service API rate limits
- **Cache when possible** - Use MCP caching features where available
- **Batch operations** - Group related API calls when supported
- **Connection pooling** - Leverage persistent connections for HTTP transport

### Maintenance Workflows
```bash
# Weekly maintenance
claude mcp list                         # Verify all connections healthy
claude mcp test --all                   # Test all server connections

# Monthly maintenance  
# Review and rotate authentication tokens
# Update to latest server versions
# Clean up unused or deprecated servers

# Troubleshooting workflow
CLAUDE_LOG=debug claude mcp list        # Debug connection issues
claude mcp remove problematic-server    # Remove failing servers
# Research latest installation instructions
# Reinstall with updated configuration
```

## Integration with Development Workflow

### Project-Specific MCP Usage
- **Document MCP dependencies** in project CLAUDE.md files
- **Include MCP server requirements** in project setup instructions
- **Version pin MCP servers** for reproducible development environments
- **Test MCP integrations** as part of project CI/CD if applicable

### Tool Integration
- **Combine with chezmoi** - Version control MCP configurations
- **Use with 1Password** - Secure credential management
- **Integrate with git hooks** - Validate MCP connections before commits
- **Monitor with logging** - Track MCP usage and performance

This module ensures consistent, secure, and reliable MCP server installation and management following established best practices.