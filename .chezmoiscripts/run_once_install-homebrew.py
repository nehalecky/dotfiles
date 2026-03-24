#!/usr/bin/env python3
"""Install Homebrew package manager if not already present."""
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

BREW_INSTALL_URL = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
BREW_PATHS = [
    Path("/opt/homebrew/bin/brew"),  # Apple Silicon
    Path("/usr/local/bin/brew"),     # Intel
]


def find_brew() -> Optional[Path]:
    for p in BREW_PATHS:
        if p.exists():
            return p
    return None


def main() -> None:
    print("🍺 Checking Homebrew installation...")

    if shutil.which("brew"):
        print("✅ Homebrew is already installed")
    else:
        print("Installing Homebrew...")
        # Download installer via curl (handles redirects + TLS reliably on macOS)
        fetch = subprocess.run(
            ["curl", "-fsSL", BREW_INSTALL_URL],
            capture_output=True,
            text=True,
        )
        if fetch.returncode != 0:
            print(f"❌ Failed to download Homebrew installer: {fetch.stderr}", file=sys.stderr)
            sys.exit(1)

        result = subprocess.run(["/bin/bash"], input=fetch.stdout, text=True)
        if result.returncode != 0:
            print("❌ Homebrew installation failed", file=sys.stderr)
            sys.exit(1)

        brew_path = find_brew()
        if not brew_path:
            print("❌ Homebrew installation may have failed", file=sys.stderr)
            sys.exit(1)

        arch = "Apple Silicon" if "opt/homebrew" in str(brew_path) else "Intel"
        print(f"✅ Homebrew installed successfully ({arch})")

    result = subprocess.run(["brew", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.strip().splitlines()[0]
        print(f"✨ {version} is ready!")


if __name__ == "__main__":
    main()
