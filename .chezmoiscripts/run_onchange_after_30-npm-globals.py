#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# Install global npm packages.
# Re-runs automatically when this script changes (e.g. to update package versions).
#
# To trigger a re-install after updating a package, bump the version comment below:
# claude-code: latest (npm install -g @anthropic-ai/claude-code)
import shutil
import subprocess
import sys

NPM_GLOBAL_PACKAGES = [
    "@anthropic-ai/claude-code",
]


def find_npm() -> str | None:
    if shutil.which("npm"):
        return "npm"
    # Homebrew-managed npm on macOS
    for path in ("/opt/homebrew/bin/npm", "/usr/local/bin/npm"):
        if shutil.which(path):
            return path
    return None


def main() -> None:
    print("📦 Installing global npm packages...")

    npm = find_npm()
    if not npm:
        print("❌ npm not found — skipping global npm package installation", file=sys.stderr)
        sys.exit(1)

    print(f"✅ npm found at: {shutil.which(npm) or npm}")

    for package in NPM_GLOBAL_PACKAGES:
        print(f"📦 Installing {package}...")
        result = subprocess.run(
            [npm, "install", "-g", package],
            capture_output=False,  # stream output so progress is visible
        )
        if result.returncode != 0:
            print(f"❌ Failed to install {package}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ {package} installed successfully")

    print("✨ Global npm packages ready!")


if __name__ == "__main__":
    main()
