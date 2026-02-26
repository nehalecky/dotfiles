# iTerm2 Configuration

This directory contains iTerm2 preferences and profiles managed by chezmoi using Dynamic Profiles.

## How It Works

iTerm2 automatically loads JSON profiles from a **fixed location**:
```
~/Library/Application Support/iTerm2/DynamicProfiles/
```

Our setup:
1. **Stores** profiles in `~/.config/iterm2/DynamicProfiles/` (version controlled)
2. **Syncs** to iTerm2's required location via chezmoi script
3. **Auto-reloads** when files change (instant updates!)

The sync happens automatically:
- After every `chezmoi apply`
- Uses rsync for efficient updates
- Preserves all your profile customizations

## Profile-Aware Dynamic Profiles

`DynamicProfiles/default.json` is rendered from a chezmoi template (`default.json.tmpl`). The
rendered content adapts based on the active profile:

- **personal** profile: standard terminal appearance
- **work** profile: red WORK badge displayed in the terminal window for visual distinction

To inspect or modify the template:
```bash
# View the source template
bat ~/.local/share/chezmoi/dot_config/iterm2/DynamicProfiles/default.json.tmpl

# After editing the HOME file, sync to chezmoi source
chezmoi add ~/.config/iterm2/DynamicProfiles/default.json
chezmoi git -- commit -m "feat: update iTerm2 dynamic profile"
```

The profile is set once at `chezmoi init` time via `.chezmoi.toml.tmpl` and stored in
`.chezmoidata.yaml`.

## Initial Setup (One-time)

### Export Your Current Profile

1. Open iTerm2 -> Preferences -> Profiles
2. Select your profile
3. Click "Other Actions" -> "Save Profile as JSON"
4. Save to: `~/.config/iterm2/DynamicProfiles/default.json`
5. Add to chezmoi:
   ```bash
   chezmoi add ~/.config/iterm2/DynamicProfiles/default.json
   chezmoi git -- commit -m "feat: add iTerm2 profile"
   chezmoi git -- push
   ```

## New Machine Setup

Everything is automated! Just:

```bash
# Install iTerm2
brew install --cask iterm2

# Apply dotfiles (includes iTerm2 setup)
chezmoi init --apply <your-github-username>/dotfiles

# Launch iTerm2 - your profile is already loaded!
open -a iTerm
```

After `chezmoi apply`, the chezmoi scripts handle syncing profiles to iTerm2's required location.
The actual scripts that run are:

- `run_once_after_40-starship-check.sh` - validates starship prompt setup
- `run_once_install-homebrew.sh` - installs Homebrew if missing
- `run_onchange_after_20-brew-bundle.sh.tmpl` - installs Homebrew packages from Brewfile
- `run_onchange_install-starship.sh.tmpl` - installs/updates Starship prompt

## What's Included

### Preferences
- Color schemes
- Font settings
- Key mappings
- Window arrangements
- Shell integration settings

### Dynamic Profiles
Dynamic profiles can be added as JSON files in:
```
~/.config/iterm2/DynamicProfiles/
```

Example profile:
```json
{
  "Profiles": [{
    "Name": "Development",
    "Guid": "development-profile",
    "Custom Command": "No",
    "Initial Text": "echo 'Development Environment'",
    "ASCII Ligatures": true
  }]
}
```

## Customization

### Color Schemes
Popular schemes to consider:
- Dracula
- Nord
- Solarized Dark
- One Dark

### Fonts
Recommended fonts with ligature support:
- JetBrains Mono
- Fira Code
- Cascadia Code
- SF Mono (macOS default)

### Key Mappings
Common custom mappings:
- Cmd+D: Split vertically
- Cmd+Shift+D: Split horizontally
- Cmd+[/]: Navigate between panes

## Backup Strategy

The preferences file is automatically backed up by:
1. chezmoi (version controlled)
2. Time Machine (if enabled)
3. iTerm2's preference sync (if configured)

## Troubleshooting

### Preferences not loading
1. Ensure the path is correct in iTerm2 preferences
2. Check file permissions: `ls -la ~/.config/iterm2/preferences/`
3. Restart iTerm2 after changing preference location

### Missing settings
Some settings may be system-specific and not included:
- Display arrangements
- System-specific paths
- Hardware-dependent settings
