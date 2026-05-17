#!/usr/bin/env python3
# autowt-version: 0.6.0-rc3
"""Install autowt and awt binaries to ~/bin/ from GitHub releases.

Re-runs when this file changes (run_onchange). Bump the autowt-version comment
above to trigger a reinstall on the next `chezmoi apply`.

Skips if autowt is already on PATH — defers to whatever installed it (e.g.
Homebrew or mac_configure). macOS only; exits cleanly on other platforms.
"""
import platform
import shutil
import stat
import sys
import urllib.request
from pathlib import Path

AUTOWT_VERSION = "v0.6.0-rc3"
BINARIES = ["autowt", "awt"]
INSTALL_DIR = Path.home() / "bin"
BASE_URL = f"https://github.com/irskep/autowt/releases/download/{AUTOWT_VERSION}"

ARCH_MAP = {
    "arm64": "arm64",
    "aarch64": "arm64",
    "x86_64": "amd64",
    "amd64": "amd64",
}


def main() -> None:
    # macOS only
    if platform.system() != "Darwin":
        print(f"⏭️  Not macOS (got {platform.system()!r}) — skipping autowt install")
        return

    # Skip if autowt is already on PATH — defer to whatever installed it
    if shutil.which("autowt"):
        print(f"✅ autowt already on PATH ({shutil.which('autowt')}) — skipping install")
        return

    machine = platform.machine().lower()
    arch = ARCH_MAP.get(machine)
    if arch is None:
        print(f"❌ Unsupported architecture: {machine!r}", file=sys.stderr)
        sys.exit(1)

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    for binary in BINARIES:
        url = f"{BASE_URL}/{binary}-darwin-{arch}"
        dest = INSTALL_DIR / binary
        print(f"⬇️  Downloading {binary} {AUTOWT_VERSION} ({arch}) ...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as exc:
            print(f"❌ Failed to download {url}: {exc}", file=sys.stderr)
            sys.exit(1)

        # chmod +x
        current = dest.stat().st_mode
        dest.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"✅ Installed {dest}")

    print(f"🎉 autowt {AUTOWT_VERSION} ready in {INSTALL_DIR}")


if __name__ == "__main__":
    main()
