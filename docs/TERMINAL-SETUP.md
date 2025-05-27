# Terminal Setup Guide

## Overview

This repository uses WezTerm as the primary terminal emulator with a hybrid approach:
- **WezTerm** handles terminal multiplexing (splits/panes)
- **Yabai** manages application-level window tiling
- **btop** provides modern system monitoring

## Key Features

### Leader Key System
- **Leader**: `Ctrl+a` (similar to tmux)
- **Timeout**: 1000ms
- **Visual indicator**: Shows "LEADER" in status bar when active

### Pane Management

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Split Vertical | `Leader + \|` | Split pane vertically |
| Split Horizontal | `Leader + -` | Split pane horizontally |
| Navigate Left | `Leader + h` | Move to pane on the left |
| Navigate Right | `Leader + l` | Move to pane on the right |
| Navigate Up | `Leader + k` | Move to pane above |
| Navigate Down | `Leader + j` | Move to pane below |
| Resize Left | `Leader + Shift + H` | Increase pane size left |
| Resize Right | `Leader + Shift + L` | Increase pane size right |
| Resize Up | `Leader + Shift + K` | Increase pane size up |
| Resize Down | `Leader + Shift + J` | Increase pane size down |
| Close Pane | `Leader + x` | Close current pane (with confirmation) |
| Zoom Toggle | `Leader + z` | Toggle pane zoom state |

### System Monitoring

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Monitor Split | `Leader + m` | Open btop in right split (50%) |
| Monitor Window | `Leader + Shift + M` | Open btop in new window |

### iTerm2 Compatibility Shortcuts

| Action | Keybinding | Description |
|--------|-----------|-------------|
| Delete Word | `Option + Backspace` | Delete word backward |
| Beginning of Line | `Cmd + ←` | Jump to line start |
| End of Line | `Cmd + →` | Jump to line end |
| Word Left | `Option + ←` | Jump word backward |
| Word Right | `Option + →` | Jump word forward |
| Delete to Beginning | `Cmd + Backspace` | Delete to line start |
| Delete Word Forward | `Option + Delete` | Delete word forward |

### Status Bar

The status bar displays:
- **Left**: Current working directory (with `~` for home)
- **Right**: LEADER indicator when leader key is active

## Configuration Details

### Font Settings
- **Font**: MesloLGS NF (Nerd Font)
- **Size**: 12pt
- **Ligatures**: Enabled (calt, clig, liga)

### Color Scheme
- Based on Monokai/iTerm2 dark theme
- Custom ANSI colors for optimal visibility
- Hyperlink detection enabled

### Window Behavior
- **Decorations**: RESIZE (for yabai compatibility)
- **Resize Increments**: Cell-based (terminal grid)
- **Initial Size**: 80x25
- **Padding**: 2px all sides

### Performance
- **GPU Acceleration**: WebGpu frontend
- **Max FPS**: 120
- **Scrollback**: 1000 lines

## Yabai Integration

WezTerm is configured to work seamlessly with yabai:
- Uses `RESIZE` window decorations to prevent gaps
- Cell-based resizing for proper grid alignment
- No additional yabai rules needed

## Customization

The configuration file is located at `~/.wezterm.lua` and is managed by chezmoi.

To modify settings:
```bash
chezmoi edit ~/.wezterm.lua
chezmoi diff
chezmoi apply
```

## Troubleshooting

### Font Not Found
If you see font warnings, ensure MesloLGS NF is installed:
```bash
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font
```

### Pane Navigation Not Working
Ensure no other applications are intercepting `Ctrl+a`. Check:
- System keyboard shortcuts
- Other terminal multiplexers (tmux/screen)

### Status Bar Not Updating
The status bar updates every second. If not visible:
- Check `enable_tab_bar = true`
- Verify `hide_tab_bar_if_only_one_tab = false`

## Philosophy

This configuration follows the terminal-first approach:
- Minimal UI chrome for maximum screen space
- Keyboard-driven workflow
- Native performance through GPU acceleration
- Seamless integration with macOS features