# Starship Prompt Configuration

This directory contains theme files for the Starship prompt, which is managed by chezmoi.

## Overview

Starship is a minimal, blazing-fast, and infinitely customizable prompt for any shell. It's written
in Rust and provides excellent performance compared to shell prompts written in interpreted
languages.

## Features

Our configuration provides a two-line layout:

**Line 1 (Context):**
- OS icon (macOS)
- Current directory with smart truncation
- Git branch and status
- Command duration (for long-running commands)
- Current time (24h format with seconds)

**Line 2 (Input):**
- Prompt character (green on success, red on error)

## Profile-Aware Configuration

`~/.config/starship.toml` is rendered from a chezmoi template (`starship.toml.tmpl`). The template
selects theme content based on the `profile` variable set at `chezmoi init` time:

| Profile | Theme file | Cloud/k8s sections | Hostname |
|---------|-----------|---------------------|----------|
| `personal` | `themes/personal.toml` | disabled (aws, kubernetes) | hidden |
| `work` | `themes/work.toml` | kubernetes context shown, AWS profile shown | displayed |

The profile is determined once at machine setup and stored in `.chezmoidata.yaml`. It is not
intended to be changed at runtime.

### Themes directory

```
~/.config/starship/themes/
  personal.toml   # minimal theme — no cloud/k8s clutter
  work.toml       # full context — k8s namespace, AWS profile, hostname
```

## Configuration

`~/.config/starship.toml` is a generated file — **do not edit it directly**. It will be
overwritten on the next `chezmoi apply`.

To make permanent changes, edit the source template:

```bash
# 1. Edit the rendered file in HOME as a starting point
#    (changes here are temporary until chezmoi apply)
vim ~/.config/starship.toml

# 2. Once happy, copy changes into the chezmoi source template
vim ~/.local/share/chezmoi/dot_config/starship.toml.tmpl

# 3. Or edit a theme file directly
vim ~/.config/starship/themes/personal.toml
chezmoi add ~/.config/starship/themes/personal.toml
chezmoi git -- commit -m "feat: update personal starship theme"
```

### Machine-Specific Settings

Edit `~/.local/share/chezmoi/.chezmoidata.yaml` to customize prompt behavior:

```yaml
starship:
  show_time: true
  show_kubernetes: false
  git_truncation: 20
  dir_truncation: 3
  prompt_theme: "p10k"
```

Note: `prompt_theme` is a legacy key from the Powerlevel10k era. Starship is now the sole prompt.

## Performance

Starship is significantly faster than Powerlevel10k:
- 5-10x faster prompt rendering
- Written in Rust for maximum performance
- Lower memory footprint
- Better battery life on laptops

## Troubleshooting

### Prompt not showing correctly

1. Ensure you have a Nerd Font installed
2. Check that your terminal supports Unicode
3. Verify Starship is installed: `starship --version`

### Git status not updating

- Starship uses libgit2 for fast git operations
- Large repositories might need: `git config core.fsmonitor true`

### Time not showing

- Check that `time.disabled = false` in the configuration
- The time module is on the right side of line 1

### Work context not showing (k8s / AWS)

- Confirm your profile is set to `work` in `.chezmoidata.yaml`
- Re-run `chezmoi apply` to re-render `starship.toml` from the template

## Resources

- [Starship Documentation](https://starship.rs/)
- [Configuration Reference](https://starship.rs/config/)
- [Preset Gallery](https://starship.rs/presets/)
