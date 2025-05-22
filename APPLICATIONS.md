# Applications & Tools Documentation

This document provides a comprehensive overview of all applications and command-line tools managed through Homebrew in this dotfiles setup.

## Table of Contents
- [Command-Line Tools (Formulae)](#command-line-tools-formulae)
  - [Core Development](#core-development)
  - [Terminal Enhancement](#terminal-enhancement)
  - [Development Utilities](#development-utilities)
  - [Other Tools](#other-tools)
- [Desktop Applications (Casks)](#desktop-applications-casks)
  - [Development & Programming](#development--programming)
  - [Security & Privacy](#security--privacy)
  - [Productivity & Knowledge](#productivity--knowledge)
  - [Communication](#communication)
  - [Internet & Browsers](#internet--browsers)
  - [Media & Entertainment](#media--entertainment)
  - [Utilities & System Tools](#utilities--system-tools)

## Command-Line Tools (Formulae)

### Core Development

| Tool | Category | Description | Enhances/Replaces |
|------|----------|-------------|-------------------|
| [git](https://git-scm.com/) | Version Control | Distributed version control system | Stock macOS git (older) |
| [gh](https://cli.github.com/) | GitHub Integration | GitHub's official CLI for pull requests, issues, and more | Web-based GitHub workflow |
| [docker](https://www.docker.com/) | Containerization | Container platform (CLI only, requires Docker Desktop) | Virtual machines |
| [node](https://nodejs.org/) | JavaScript Runtime | JavaScript runtime built on Chrome's V8 engine | System node (if any) |
| [jq](https://stedolan.github.io/jq/) | JSON Processing | Lightweight JSON processor with powerful filters | Manual JSON parsing |
| [pdm](https://pdm.fming.dev/) | Python Development | Modern Python package manager with PEP 582 support | pip/pipenv/poetry |

### Terminal Enhancement

| Tool | Category | Description | Enhances/Replaces |
|------|----------|-------------|-------------------|
| [zsh](https://www.zsh.org/) | Shell | Z shell - powerful shell with better completion | bash (default macOS shell) |
| [bash](https://www.gnu.org/software/bash/) | Shell | GNU Bourne Again Shell | macOS bash (v3.x, outdated) |
| [starship](https://starship.rs/) | Shell Prompt | Fast, customizable, cross-shell prompt | prezto prompts, powerlevel10k |
| [bat](https://github.com/sharkdp/bat) | File Viewer | cat clone with syntax highlighting and Git integration | cat |
| [eza](https://eza.rocks/) | Directory Listing | Modern ls replacement with colors, icons, and Git status | ls |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | Text Search | Blazingly fast recursive grep with smart defaults | grep, ag, ack |
| [fzf](https://github.com/junegunn/fzf) | Fuzzy Finder | Command-line fuzzy finder for files, history, processes | Traditional file search |
| [glow](https://github.com/charmbracelet/glow) | Markdown Viewer | Render markdown on the CLI with style | less/cat for .md files |
| [tealdeer](https://github.com/dbrgn/tealdeer) | Help Pages | Fast tldr client - simplified man pages | man pages (supplements) |
| [btop](https://github.com/aristocratos/btop) | System Monitor | Beautiful resource monitor with mouse support | htop, top |
| [wget](https://www.gnu.org/software/wget/) | File Download | Non-interactive network downloader | curl (different features) |

### Development Utilities

| Tool | Category | Description | Enhances/Replaces |
|------|----------|-------------|-------------------|
| [emacs](https://www.gnu.org/software/emacs/) | Text Editor | Extensible, customizable text editor | vim, nano |
| [cosign](https://github.com/sigstore/cosign) | Security | Container signing and verification | Manual verification |
| [flux](https://fluxcd.io/) | GitOps | Continuous delivery tool for Kubernetes | Manual deployments |
| [chezmoi](https://www.chezmoi.io/) | Dotfiles Manager | Manage dotfiles across multiple machines | Bare git repos, stow |

### Other Tools

| Tool | Category | Description | Enhances/Replaces |
|------|----------|-------------|-------------------|
| [llm](https://llm.datasette.io/) | AI/ML | CLI for interacting with Large Language Models | Web-based AI interfaces |
| [speedtest-cli](https://www.speedtest.net/apps/cli) | Network Testing | Command-line interface for testing internet bandwidth | Web-based speed tests |

## Desktop Applications (Casks)

### Development & Programming

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [Visual Studio Code](https://code.visualstudio.com/) | Code Editor | Extensible code editor with IntelliSense, debugging, Git | Primary code editor with vast extension ecosystem |
| [Cursor](https://cursor.sh/) | AI Code Editor | AI-first code editor built on VSCode | AI-assisted coding, pair programming with AI |
| [iTerm2](https://iterm2.com/) | Terminal Emulator | Advanced terminal with split panes, search, autocomplete | Enhanced terminal experience vs Terminal.app |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Containerization | Docker with GUI, Kubernetes, and development tools | Container development and management |
| [Julia](https://julialang.org/) | Scientific Computing | High-performance language for technical computing | Scientific computing, data science |
| [Miniconda](https://docs.conda.io/en/latest/miniconda.html) | Python Environment | Minimal conda installer for Python environments | Python version and package management |
| [TeXShop](https://pages.uoregon.edu/koch/texshop/) | LaTeX Editor | LaTeX editor and PDF previewer for macOS | Academic writing, technical documents |
| [GitHub Desktop](https://desktop.github.com/) | Git GUI | Visual Git client by GitHub | Visual git workflow (optional with CLI) |

### Security & Privacy

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [1Password](https://1password.com/) | Password Manager | Password manager with SSH agent and CLI integration | Secure credential storage and SSH key management |
| [1Password CLI](https://developer.1password.com/docs/cli/) | CLI Tool | Command-line interface for 1Password | Scripting, automation, SSH agent |
| [GPG Suite](https://gpgtools.org/) | Encryption | GPG tools for mail encryption and file signing | Email encryption, commit signing |
| [ProtonVPN](https://protonvpn.com/) | VPN | Privacy-focused VPN service | Secure browsing, privacy protection |

### Productivity & Knowledge

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [Obsidian](https://obsidian.md/) | Note-Taking | Knowledge base with linked notes and markdown | Personal knowledge management, note-taking |
| [Raycast](https://www.raycast.com/) | Launcher | Extensible launcher with snippets, scripts, extensions | Replaces Spotlight, Alfred |
| [Zotero](https://www.zotero.org/) | Reference Manager | Research reference and citation manager | Academic research, bibliography management |
| [Claude](https://claude.ai/) | AI Assistant | Anthropic's AI assistant desktop app | AI-powered assistance and chat |

### Communication

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [Slack](https://slack.com/) | Team Chat | Team communication and collaboration platform | Work communication, community channels |
| [Signal](https://signal.org/) | Secure Messaging | Privacy-focused encrypted messaging | Secure personal communication |
| [Telegram](https://telegram.org/) | Messaging | Cloud-based messaging with channels and bots | Groups, channels, file sharing |
| [WhatsApp](https://www.whatsapp.com/) | Messaging | Popular messaging platform | Personal messaging, international communication |
| [Zoom](https://zoom.us/) | Video Conferencing | Video meetings and webinars | Remote meetings, presentations |

### Internet & Browsers

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [Arc](https://arc.net/) | Browser | Innovative browser with spaces and sidebar | Modern browsing with better organization |
| [Firefox](https://www.mozilla.org/firefox/) | Browser | Privacy-focused open source browser | Alternative browser, privacy features |

### Media & Entertainment

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [Spotify](https://www.spotify.com/) | Music Streaming | Music streaming service | Music listening and discovery |
| [VLC](https://www.videolan.org/vlc/) | Media Player | Universal media player supporting all formats | Video/audio playback for any format |
| [Sonic Pi](https://sonic-pi.net/) | Music Programming | Code-based music creation and performance tool | Live coding music, education |
| [Steam](https://store.steampowered.com/) | Gaming Platform | Digital game distribution platform | Gaming, game library management |
| [Pokemon TCG Online](https://www.pokemon.com/us/pokemon-tcg/play-online/) | Gaming | Official Pokemon Trading Card Game | Digital card game |

### Utilities & System Tools

| Application | Category | Description | Use Case |
|-------------|----------|-------------|----------|
| [OpenMTP](https://openmtp.ganeshrvel.com/) | File Transfer | Android file transfer for macOS | Transfer files to/from Android devices |
| [Garmin Express](https://www.garmin.com/en-US/software/express/) | Device Sync | Sync and update Garmin devices | Garmin device management |
| [QR Journal](https://www.joshjacob.com/mac-development/qrjournal.php) | QR Tools | QR code scanner using Mac's camera | Quick QR code scanning |
| [Font Awesome Terminal](https://github.com/gabrielelana/awesome-terminal-fonts) | Fonts | Icon fonts for terminal | Terminal icons and symbols |

## Installation Notes

### Using the Brewfile
```bash
# Install all applications and tools
brew bundle

# Install only formulae
brew bundle --no-cask

# Check what would be installed
brew bundle check --verbose
```

### Categories Overview

**Essential Development Stack:**
- Version control: git + gh
- Containerization: Docker Desktop + docker CLI
- Code editors: VS Code and/or Cursor
- Terminal: iTerm2 + enhanced CLI tools
- Package management: Homebrew + language-specific tools

**Productivity Enhancement:**
- Terminal improvements: starship, bat, eza, ripgrep, fzf
- Knowledge management: Obsidian
- System launcher: Raycast
- Password management: 1Password

**Optional Tools:**
- Specialized editors: Emacs, TeXShop
- Scientific computing: Julia, Miniconda
- Entertainment: Spotify, Steam, VLC
- Additional browsers: Arc, Firefox

## Maintenance Tips

1. **Regular Updates**: Keep tools updated with `brew upgrade`
2. **Dependency Check**: Use `brew deps --tree` to understand dependencies
3. **Cleanup**: Remove unused tools with `brew bundle cleanup`
4. **Documentation**: Update this file when adding/removing tools

## Philosophy

This setup prioritizes:
- **Enhanced defaults**: Better versions of standard Unix tools
- **Developer productivity**: Tools that speed up common tasks
- **Security**: Password management and encryption tools
- **Flexibility**: Multiple options for editors and browsers
- **Modern workflows**: Git integration, containerization, AI assistance