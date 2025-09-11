# WeeChat IRC Client Setup Guide

## Overview

WeeChat is configured with advanced security and privacy features including Tor proxy anonymization, TLS encryption, and anonymous nicknames. This guide covers completing the initial setup and basic usage.

## Security Features Implemented

- **Tor Anonymization**: All IRC traffic routed through Tor SOCKS5 proxy (127.0.0.1:9050)
- **Anonymous Nicknames**: Uses generic names (anon, anon1, anon2, etc.) instead of identifying information
- **Strong TLS Encryption**: TLS 1.2+ with secure cipher suites for server connections
- **Certificate Verification**: SSL/TLS certificate validation enabled
- **Privacy-Focused Logging**: Auto-logging disabled to prevent chat history storage
- **No Personal Information**: Username and realname set to "anon" and "Anonymous"

## Prerequisites

Ensure Tor is installed and running:

```bash
# Check if Tor is running
brew services list | grep tor

# Start Tor if not running
brew services start tor

# Verify security setup
~/.config/weechat/verify_security.sh
```

## Initial Setup (5 Commands)

After launching WeeChat for the first time, you need to run these commands to complete the secure configuration:

### 1. Launch WeeChat
```bash
weechat
```

### 2. Execute Setup Commands

Copy and paste these commands into WeeChat one by one:

```irc
# Create secure proxy configuration
/proxy add tor socks5 127.0.0.1 9050

# Add Libera.Chat server with security settings
/server add libera irc.libera.chat/6697 -ssl -autoconnect
/set irc.server.libera.proxy "tor"
/set irc.server.libera.nicks "anon,anon1,anon2,anon3,anon4"
/set irc.server.libera.username "anon"
```

### 3. Complete Configuration

```irc
# Additional security settings
/set irc.server.libera.realname "Anonymous"
/set irc.server.libera.tls on
/set irc.server.libera.tls_verify on
/set irc.server.libera.tls_priorities "SECURE256:+SECURE128:-VERS-ALL:+VERS-TLS1.2:+VERS-TLS1.3"
/set irc.server.libera.capabilities "account-notify,away-notify,cap-notify,multi-prefix,server-time"
```

### 4. Privacy Settings

```irc
# Remove quit/part messages for privacy
/set irc.server.libera.msg_quit ""
/set irc.server.libera.msg_part ""

# Global security settings
/set weechat.network.proxy_curl ""
/set logger.file.auto_log off
/set weechat.look.save_config_on_exit on
```

### 5. Save and Connect

```irc
# Save configuration
/save

# Connect to Libera.Chat
/connect libera
```

## Basic Usage

### Essential Commands

```irc
# Join a channel
/join #channel-name

# Send a private message
/msg nickname message

# Change nickname
/nick new-nickname

# List channels on server
/list

# Get help
/help
/help command-name

# Quit WeeChat
/quit
```

### Navigation

- **Alt + ←/→**: Switch between buffers
- **Alt + A**: Jump to buffer with activity
- **Alt + J**: Jump to buffer by number
- **Ctrl + C**: Cancel current input
- **Page Up/Down**: Scroll chat history

### Channel Management

```irc
# Join channels
/join #libera
/join #weechat

# Part (leave) channel
/part
/part #channel-name

# Set topic
/topic New channel topic

# Channel modes
/mode #channel +m  # Moderated
/mode #channel -m  # Remove moderated
```

## Configuration Files

WeeChat configuration is stored in `~/.config/weechat/`:

- **weechat.conf**: Main WeeChat configuration
- **irc.conf**: IRC plugin settings and server configurations
- **logger.conf**: Logging settings (auto-log disabled for privacy)
- **startup_commands.txt**: Reference commands for initial setup
- **verify_security.sh**: Security verification script

## Security Verification

Run the security verification script to check your setup:

```bash
~/.config/weechat/verify_security.sh
```

This script verifies:
- Tor service is running
- SOCKS proxy is listening
- Configuration files are present
- Proxy configuration is active

## Troubleshooting

### Common Issues

**1. Connection Fails**
```irc
# Check proxy status
/proxy

# Test connection without proxy temporarily
/set irc.server.libera.proxy ""
/reconnect libera

# Re-enable proxy
/set irc.server.libera.proxy "tor"
```

**2. Tor Not Working**
```bash
# Restart Tor service
brew services restart tor

# Check Tor logs
brew services list | grep tor
```

**3. Certificate Errors**
```irc
# Check TLS settings
/set irc.server.libera.tls*

# Temporarily disable certificate verification (not recommended)
/set irc.server.libera.tls_verify off
```

**4. Nickname Issues**
```irc
# Use different nickname
/nick anon2

# Check current nick
/me

# Register nickname (if desired)
/msg NickServ REGISTER password email@example.com
```

### Debug Commands

```irc
# Show current server settings
/set irc.server.libera.*

# Show proxy settings
/proxy

# Check connection status
/server

# Display buffer information
/buffer
```

## Advanced Features

### Scripts and Plugins

WeeChat supports Python, Perl, Ruby, Lua, and Tcl scripts:

```irc
# Install script manager
/script install go.py

# List available scripts
/script search keyword

# Install a script
/script install script-name.py
```

### Relay (Remote Interface)

Configure WeeChat relay for remote access:

```irc
# Set relay password
/set relay.network.password mypassword

# Enable IRC relay
/relay add irc.ssl 9001

# Enable WeeChat protocol relay
/relay add weechat 9000
```

### Filters

Create filters to hide unwanted messages:

```irc
# Hide join/part/quit messages
/filter add joinquit * irc_join,irc_part,irc_quit *

# Hide nick changes
/filter add nickchange * irc_nick *

# List filters
/filter
```

## Privacy Best Practices

1. **Use Anonymous Nicknames**: Avoid personally identifiable nicknames
2. **Disable Logging**: Keep `logger.file.auto_log` set to `off`
3. **Clear History**: Regularly clear buffer history with `/buffer clear`
4. **Verify Tor**: Always ensure Tor is running before connecting
5. **Use TLS**: Only connect to servers supporting SSL/TLS
6. **No Personal Info**: Avoid sharing identifying information in chats

## Integration with Dotfiles

WeeChat configuration is managed by chezmoi dotfiles system:

```bash
# View managed files
chezmoi managed | grep weechat

# Apply configuration changes
chezmoi apply

# Check configuration diff
chezmoi diff ~/.config/weechat/
```

## Resources

- **Official Documentation**: https://weechat.org/doc/
- **Quick Start Guide**: https://weechat.org/doc/weechat/quickstart/
- **User Guide**: https://weechat.org/doc/weechat/user/
- **Plugin API**: https://weechat.org/doc/weechat/plugin/
- **Scripts Repository**: https://weechat.org/scripts/

## Support

For issues with this configuration:
1. Run `~/.config/weechat/verify_security.sh`
2. Check WeeChat logs in the application
3. Verify Tor service status
4. Test connection without proxy to isolate issues

Remember: All IRC traffic is anonymized through Tor when properly configured!