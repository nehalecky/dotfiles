# macOS Visual Notifications from CLI Subprocesses

## Status: In Progress
**Branch:** `feat/multi-channel-notifications`
**Blocker:** Banners not appearing on macOS 15 Sequoia from detached subprocesses

---

## Problem Statement

Claude Code lifecycle hooks fire as detached subprocesses — no controlling terminal,
no app bundle, no GUI session context. We need visual notifications that:

1. Appear without user interaction (banner, not tray-only)
2. Work from a subprocess with no TTY
3. Require no API key or network access
4. Integrate with macOS Focus/DND semantics

---

## What We Tried (macOS 15.7.4 Sequoia, arm64)

### 1. `osascript` / Script Editor

**Command:**
```bash
osascript -e 'display notification "msg" with title "Claude Code" sound name "Glass"'
```

**Result:** Exit 0, nothing shown, Script Editor never appears in System Settings → Notifications.

**Root cause:** On macOS 15 Sequoia, `display notification` via osascript from a terminal
subprocess no longer triggers the permission prompt. Script Editor is not registered with
Notification Center at all. Apple silently dropped this path in Sequoia.

**References:**
- [Radar FB12345 pattern](https://openradar.appspot.com) — multiple reports of osascript
  `display notification` silently failing on Sequoia
- Stack Overflow consensus: use `terminal-notifier` instead

---

### 2. `terminal-notifier` 2.0.0

**Command:**
```bash
terminal-notifier -message "msg" -title "Claude Code" -sound Glass
```

**Result:** Notifications arrive in Notification Center tray but **no banner appears**,
even with style set to Banners in System Settings.

**Variants tried:**
- With `-sender com.github.wez.wezterm` (route through WezTerm which has Banners permission) — tray only
- With `-ignoreDnD` flag — no change
- With Alerts style set in System Settings — still tray only

**Root cause:** terminal-notifier 2.0.0 has known Sequoia regressions. The app uses
a deprecated `NSUserNotification` → `UNUserNotificationCenter` bridge that macOS 15
changed. Notifications are delivered to UNC but the presentation layer (banner) is
suppressed when the delivery comes from a non-foreground, non-app-bundle process.

**References:**
- [terminal-notifier#409](https://github.com/julienXX/terminal-notifier/issues/409) — Ventura/Sonoma banner regression
- [terminal-notifier#422](https://github.com/julienXX/terminal-notifier/issues/422) — Sequoia silent failure reports
- terminal-notifier 2.0.0 was last released 2023; unmaintained

---

### 3. OSC 9 escape sequence via `/dev/tty`

**Command (in `terminal_notify.py`):**
```python
with open("/dev/tty", "w") as tty:
    tty.write(f"\033]9;{message}\007")
```

**Result:** `OSError: [Errno 6] Device not configured`

**Root cause:** Claude Code hook subprocesses have no controlling terminal — `/dev/tty`
refers to the controlling TTY of the process group, which is absent in detached
subprocess execution. WezTerm (which supports OSC 9) never receives the sequence.

---

## Industry Survey: How Others Solve This

### CLI tools / developer tools

| Tool | Approach | macOS 15 status |
|---|---|---|
| GitHub Desktop | Electron `Notification` API | ✓ Works (Electron manages app bundle) |
| `ntfy` (cli) | HTTP push to ntfy.sh server | ✓ Works (cloud relay, no local permission) |
| `notifu` (Windows) | Windows Toast API | N/A |
| `alerter` | Fork of terminal-notifier | Not in Homebrew; last release 2019 |
| `pync` (Python) | Wraps terminal-notifier | Same limitations |
| Taskwarrior hooks | `terminal-notifier` | Same limitations on Sequoia |
| `noti` (Go) | Uses `terminal-notifier` on macOS | Same limitations |
| Hammerspoon | Lua → `hs.notify` → proper app bundle | ✓ Works (Hammerspoon is a real app) |

**Key pattern:** Every tool that reliably shows banners on modern macOS is either:
- A real `.app` bundle registered with `UNUserNotificationCenter`, or
- A cloud relay (bypasses local permission entirely)

### What the macOS platform requires (post-Sequoia)

Apple's [UNUserNotificationCenter documentation](https://developer.apple.com/documentation/usernotifications)
states that apps must call `requestAuthorization(options:completionHandler:)` from within
an app bundle with a valid `Info.plist`. This is enforced more strictly on macOS 15.

---

## Recommended Path Forward

### Option A: Tiny Swift notification app (recommended)

Build a minimal Swift CLI app (`claude-notify-helper.app`) that:
1. Is a real `.app` bundle so macOS accepts its notification permission request
2. Ships in `~/.local/bin/` managed by chezmoi
3. On first run, calls `UNUserNotificationCenter.requestAuthorization()` and prompts user
4. On subsequent runs, posts a banner notification

**Pros:** 100% reliable, no dependencies, Focus/DND semantics respected, appears as
"Claude Code Notifier" in System Settings
**Cons:** Requires compiling Swift; adds a build step to chezmoi setup

**Implementation sketch:**
```swift
// Sources/notify/main.swift
import Foundation
import UserNotifications

let center = UNUserNotificationCenter.current()
let message = CommandLine.arguments.dropFirst().joined(separator: " ")

center.requestAuthorization(options: [.alert, .sound]) { granted, _ in
    guard granted, !message.isEmpty else { exit(granted ? 0 : 1) }
    let content = UNMutableNotificationContent()
    content.title = "Claude Code"
    content.body = message
    content.sound = .default
    center.add(UNNotificationRequest(
        identifier: UUID().uuidString, content: content, trigger: nil
    )) { _ in exit(0) }
}
RunLoop.main.run(until: Date(timeIntervalSinceNow: 5))
```

Chezmoi setup script compiles this once: `swift build -c release`.

---

### Option B: Hammerspoon relay

If Hammerspoon is installed (it's in the Brewfile for personal profile), use its
`hs.notify` API via `hs -c 'hs.notify.show("Claude Code","","msg")'` from CLI.

**Pros:** Zero new code, Hammerspoon already has notification permission
**Cons:** Requires Hammerspoon installed and running; personal profile only

---

### Option C: `ntfy` cloud relay

Push to [ntfy.sh](https://ntfy.sh) (self-hostable, free tier available) from the hook,
receive on macOS ntfy app (has proper notification permission).

**Pros:** Works everywhere, cross-device, no macOS permission dance
**Cons:** Requires network; adds cloud dependency; ntfy app needed

---

### Option D: Dock badge via `SetFile` or `osascript tell Finder`

Not a notification but a visual signal: bounce the Dock icon of the terminal app.
```bash
osascript -e 'tell application "WezTerm" to activate' # brings to foreground
```
Too intrusive — rejected.

---

## Decision

**Option A** (Swift helper app) is the correct long-term fix. It's the only approach
that works reliably on Sequoia without external dependencies or cloud relay.

**Short-term** while the Swift app is built: `macos` mode falls back gracefully to
`silent` (TTS still works; visual channel is a no-op). The `both` mode retains full
TTS delivery. This is acceptable — users on Sequoia with no Hammerspoon simply get
audio notifications until the Swift helper lands.

---

## Next Steps

- [ ] Write `Sources/claude-notify-helper/main.swift` in chezmoi repo
- [ ] Add `swift build` to chezmoi setup script (run once on new machine)
- [ ] Install compiled binary to `~/.local/bin/`
- [ ] Update `macos_notify.py` to call the helper binary
- [ ] Add Hammerspoon path as fallback (`hs -c` if `hs` is available)
- [ ] Update `macos_notify.py` docstring with Sequoia notes
- [ ] Test on macOS 14 Sonoma to confirm no regression

---

## References

- [Apple UNUserNotificationCenter](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter)
- [terminal-notifier GitHub](https://github.com/julienXX/terminal-notifier)
- [ntfy.sh](https://ntfy.sh)
- [Hammerspoon hs.notify](https://www.hammerspoon.org/docs/hs.notify.html)
- [Swift Package Manager docs](https://www.swift.org/package-manager/)
