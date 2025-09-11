#!/usr/bin/env python3
"""
WeeChat Secure IRC Setup Script
Provides commands for secure, anonymous IRC connections
"""

def secure_libera_setup():
    """Setup secure connection to Libera.Chat with Tor"""
    commands = [
        # Create secure server with Tor proxy
        "/server add libera irc.libera.chat/6697 -ssl -autoconnect",
        
        # Configure Tor proxy
        "/set irc.server.libera.proxy tor",
        
        # Use anonymous nicknames
        "/set irc.server.libera.nicks anon,anon1,anon2,anon3",
        "/set irc.server.libera.username anon",
        "/set irc.server.libera.realname Anonymous",
        
        # Enable strong SSL/TLS
        "/set irc.server.libera.tls on",
        "/set irc.server.libera.tls_verify on",
        "/set irc.server.libera.tls_priorities SECURE256:+SECURE128:-VERS-ALL:+VERS-TLS1.2:+VERS-TLS1.3",
        
        # Security capabilities
        "/set irc.server.libera.capabilities account-notify,away-notify,cap-notify,multi-prefix,server-time",
        
        # Privacy settings
        "/set irc.server.libera.msg_quit",
        "/set irc.server.libera.msg_part",
        
        # Save configuration
        "/save"
    ]
    return commands

def secure_oftc_setup():
    """Setup secure connection to OFTC with Tor"""
    commands = [
        # Create secure server with Tor proxy  
        "/server add oftc irc.oftc.net/6697 -ssl",
        
        # Configure Tor proxy
        "/set irc.server.oftc.proxy tor",
        
        # Use anonymous nicknames
        "/set irc.server.oftc.nicks anon,anon1,anon2,anon3",
        "/set irc.server.oftc.username anon", 
        "/set irc.server.oftc.realname Anonymous",
        
        # Enable strong SSL/TLS
        "/set irc.server.oftc.tls on",
        "/set irc.server.oftc.tls_verify on",
        "/set irc.server.oftc.tls_priorities SECURE256:+SECURE128:-VERS-ALL:+VERS-TLS1.2:+VERS-TLS1.3",
        
        # Save configuration
        "/save"
    ]
    return commands

# Print setup instructions
if __name__ == "__main__":
    print("WeeChat Secure IRC Setup")
    print("=" * 40)
    print("\n1. Start WeeChat: weechat")
    print("\n2. For Libera.Chat, run these commands:")
    for cmd in secure_libera_setup():
        print(f"   {cmd}")
    
    print("\n3. For OFTC, run these commands:")
    for cmd in secure_oftc_setup():
        print(f"   {cmd}")
    
    print("\n4. Connect: /connect libera")
    print("5. Join channels: /join #channel")
    print("\nAll traffic will be routed through Tor for anonymity!")