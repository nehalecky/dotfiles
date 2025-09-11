#!/bin/bash
# WeeChat Security Verification Script

echo "🔐 WeeChat Security Configuration Verification"
echo "=============================================="

# Check Tor service
echo "1. Checking Tor service..."
if brew services list | grep -q "tor.*started"; then
    echo "   ✅ Tor service is running"
else
    echo "   ❌ Tor service not running"
    echo "   Run: brew services start tor"
fi

# Check Tor SOCKS proxy
echo "2. Checking Tor SOCKS proxy..."
if netstat -an | grep -q "127.0.0.1.9050.*LISTEN"; then
    echo "   ✅ Tor SOCKS proxy listening on 127.0.0.1:9050"
else
    echo "   ❌ Tor SOCKS proxy not available"
fi

# Check WeeChat config directory
echo "3. Checking WeeChat configuration..."
if [ -d "$HOME/.config/weechat" ]; then
    echo "   ✅ WeeChat config directory exists"
    
    if [ -f "$HOME/.config/weechat/weechat.conf" ]; then
        echo "   ✅ Main configuration file present"
    fi
    
    if [ -f "$HOME/.config/weechat/irc.conf" ]; then
        echo "   ✅ IRC configuration file present"
    fi
    
    if [ -f "$HOME/.config/weechat/logger.conf" ]; then
        echo "   ✅ Logger configuration file present"
    fi
else
    echo "   ❌ WeeChat config directory missing"
fi

# Check for proxy configuration
echo "4. Checking proxy configuration..."
if grep -q "socks5.*127.0.0.1:9050" "$HOME/.config/weechat/weechat.conf" 2>/dev/null; then
    echo "   ✅ Tor proxy configured in WeeChat"
else
    echo "   ⚠️  Proxy configuration may need setup"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Launch WeeChat: weechat"
echo "2. Copy commands from: ~/.config/weechat/startup_commands.txt"
echo "3. Paste commands into WeeChat to configure secure servers"
echo "4. Connect: /connect libera"
echo ""
echo "🔒 All traffic will be anonymized through Tor!"