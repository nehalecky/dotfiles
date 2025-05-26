# Starship Prompt Configuration

This directory contains the Starship prompt configuration, migrated from Powerlevel10k.

## Overview

Starship is a minimal, blazing-fast, and infinitely customizable prompt for any shell. It's written in Rust and provides excellent performance compared to traditional shell prompts.

## Features

Our configuration replicates the Powerlevel10k two-line layout:

**Line 1 (Context):**
- 🍎 OS icon (macOS)
- 📁 Current directory with smart truncation
- 🌿 Git branch and status
- ⏱️  Command duration (for long-running commands)
- 🕐 Current time (24h format with seconds)

**Line 2 (Input):**
- ❯ Prompt character (green on success, red on error)

## Configuration

The main configuration is in `~/.config/starship.toml`, which is managed by chezmoi as a template.

### Machine-Specific Settings

Edit `~/.local/share/chezmoi/.chezmoidata.yaml` to customize:

```yaml
starship:
  profile: "personal"  # or "work"
  show_time: true
  show_kubernetes: false
  prompt_theme: "starship"  # or "p10k" during migration
```

## Switching Between Prompts

During the migration period, you can switch between Starship and Powerlevel10k:

```bash
# Switch to Starship
prompt_switch starship
exec zsh

# Switch back to Powerlevel10k
prompt_switch p10k
exec zsh

# Check current prompt
prompt_switch
```

## Performance

Starship is significantly faster than Powerlevel10k:
- ⚡ 5-10x faster prompt rendering
- 🚀 Written in Rust for maximum performance
- 💾 Lower memory footprint
- 🔋 Better battery life on laptops

## Customization

To customize the prompt:

1. Edit the template: `chezmoi edit ~/.config/starship.toml`
2. Preview changes: `chezmoi diff`
3. Apply changes: `chezmoi apply`

## Troubleshooting

### Prompt not showing correctly

1. Ensure you have a Nerd Font installed (you already have this for P10k)
2. Check that your terminal supports Unicode
3. Verify Starship is installed: `starship --version`

### Git status not updating

- Starship uses libgit2 for fast git operations
- Large repositories might need: `git config core.fsmonitor true`

### Time not showing

- Check that `time.disabled = false` in the configuration
- The time module is on the right side of line 1

## Resources

- [Starship Documentation](https://starship.rs/)
- [Configuration Reference](https://starship.rs/config/)
- [Preset Gallery](https://starship.rs/presets/)

## Migration Notes

This configuration was migrated from Powerlevel10k to maintain the same visual layout while gaining Starship's performance benefits. The original P10k configuration is preserved at `~/.p10k.zsh` as a backup.